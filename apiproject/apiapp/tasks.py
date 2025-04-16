"""
Celery tasks (for text processing logic).
"""

from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from apiproject.celery import app

from .models import Call
from .processing import *


@app.task
def process_file(call_id, audio_url: str):
    """
    Does audio and text processing from provided URL and saves results to associated call.
    """
    text = get_text(audio_url)

    if text is None:
        return

    call = get_object_or_404(Call, pk=call_id)
    call.text = text
    try:
        call.emotional_tone = get_emotional_tone(text)
        call.name, call.location = get_name_and_location(text)
        call.categories.set(get_categories(text))
    finally:
        call.save()


@app.task(ignore_result=True)
def recategorize_call(call_id):
    """
    Recategorizes provided call.
    """
    call = get_object_or_404(Call, pk=call_id)

    # wait for initialization task to finish
    if call.task_id is not None:
        AsyncResult(call.task_id).get()

    if call.text is not None:
        call.categories = get_categories(call.text)
        call.save()
