import json
import wave
import vosk
import requests
from io import BytesIO
from pydub import AudioSegment
from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from apiproject.celery import app
from .pipelines import *
from .models import *


@app.task
def process_file(call_id, file):

    text = _get_text(file)

    if text is None:
        return

    call = get_object_or_404(Call, pk=call_id)
    call.text = text
    try:
        call.emotional_tone = _get_emotional_tone(text)
        call.name, call.location = _get_name_and_location(text)
        # call.categories = _get_categories(text)
    finally:
        call.save()


@app.task()
def recategorize_call(call_id):
    call = get_object_or_404(Call, pk=call_id)
    if call.task_id is not None:
        
        # wait for initiaalization task to finish
        AsyncResult(call.task_id).get()

    if call.text is not None:
        call.categories = _get_categories(call.text)
        call.save()


def _get_text(file: str):
    response = requests.get(file, stream=True)
    response.raise_for_status()

    if file.endswith(".mp3"):
        audio = AudioSegment.from_mp3(BytesIO(response.content))

        wav_stream = BytesIO()
        audio.export(wav_stream, format="wav")
        wav_stream.seek(0)

        file_stream = wav_stream
    else:
        file_stream = response.raw

    with wave.open(file_stream) as wf:
        model = vosk.Model(lang="en-us")
        rec = vosk.KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(wf.getframerate())
            if len(data) == 0:
                break

            rec.AcceptWaveform(data)

    file_stream.close()
    return json.loads(rec.FinalResult())["text"]


def _get_emotional_tone(text):
    sentiments = sentiment_pipeline(text)
    sentiment = max(sentiments, key=lambda s: float(s["score"]))["label"]

    if sentiment == "NEU":
        return EmotionalTone.NEUTRAL
    elif sentiment == "POS":
        return EmotionalTone.POSITIVE
    else:
        # if sentiment is negative - try to decide whether it is anger or just negativity
        emotions = emotions_pipeline(text)
        emotion = max(emotions[0], key=lambda s: float(s["score"]))["label"]
        if emotion == "anger":
            return EmotionalTone.ANGRY
        else:
            return EmotionalTone.NEGATIVE


def _get_name_and_location(text):
    entities = entities_pipeline(text)

    name = next((e for e in entities if e["entity_group"] == "PER"), None)
    location = next((e for e in entities if e["entity_group"] == "LOC"), None)
    return name, location


def _get_categories(text):
    categories = Category.objects.all()
    labels = [p for c in categories for p in c.points]

    result = clasify_pipeline(text, candidate_labels=labels)
    selected_labels = [label for label, score in zip(result["labels"], result["scores"]) if score >= 0.5]

    return [category for category in categories if set(category.points).issubset(selected_labels)]
