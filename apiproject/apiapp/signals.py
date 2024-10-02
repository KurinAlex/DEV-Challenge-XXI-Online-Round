"""
Database models signals (callbacks for model changes)
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

import celery

from .models import *


@receiver(post_save, sender=Category)
def handle_category_update(sender, instance: Category, **kwargs):

    # If new category was created we should recategorize all calls.
    # If category was updated, we should update only calls, associated with it.
    if kwargs["created"]:
        calls = Call.objects.all()
    else:
        calls = instance.calls

    for call in calls:
        celery.signature("apiapp.tasks.recategorize_call", args=(call.pk)).delay()
