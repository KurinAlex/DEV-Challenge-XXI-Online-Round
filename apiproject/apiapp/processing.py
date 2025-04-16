import json
import wave
import vosk
import requests
import typing

from io import BytesIO
from pydub import AudioSegment

from .models import *
from .pipelines import *


def get_text(audio_url: str) -> str:
    """
    Completes voice-to-text extraction from provided file url.
    """
    response = requests.get(audio_url, stream=True)
    response.raise_for_status()

    # convert audio to .wav format if it is presented in .mp3 format
    if audio_url.endswith(".mp3"):
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


def get_emotional_tone(text: str):
    """
    Gets emotional tone of text.
    """
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


def get_name_and_location(text: str) -> typing.Tuple[str, str]:
    """
    Gets name and location entities from text.
    """
    entities = entities_pipeline(text)

    name = next((e["word"] for e in entities if e["entity_group"] == "PER"), None)
    location = next((e["word"] for e in entities if e["entity_group"] == "LOC"), None)
    return name, location


def get_categories(text: str) -> typing.List[Category]:
    """
    Does text categorization.
    """
    categories = Category.objects.all()
    labels = [p for c in categories for p in c.points]

    result = clasify_pipeline(text, candidate_labels=labels)
    selected_labels = set([label for label, score in zip(result["labels"], result["scores"]) if score >= 0.5])

    if len(selected_labels) == 0:
        return []

    return [category for category in categories if _contains_any(category.points, selected_labels)]


def _contains_any(list_from, list_in):
    """
    Checks if any element from list_from is contained in list_in
    """
    return any(element in list_in for element in list_from)
