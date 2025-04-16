"""
Function-services for processing calls.
"""

from django.shortcuts import get_object_or_404

import celery
from celery.result import AsyncResult

from .models import *


def get_call_if_processed(call_id) -> Call | None:
    """
    Retrieves call object if its audio is processed or returns None otherwise.
    """
    call = get_object_or_404(Call, pk=call_id)
    result = AsyncResult(call.task_id)

    if result.ready():
        return call
    else:
        return None


def post_call(audio_url: str):
    """
    Posts audio URL for processing and returns created call id.
    """
    task_id = celery.uuid()
    call = Call.objects.create(task_id=task_id)

    celery.signature("apiapp.tasks.process_file", args=(call.pk, audio_url)).apply_async(task_id=task_id)

    return call.pk
