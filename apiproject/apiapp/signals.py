from django.db.models.signals import post_save
from django.dispatch import receiver

from celery import uuid

from .models import *
from .tasks import recategorize_call


@receiver(post_save, sender=Category)
def handle_category_update(sender, instance: Category, **kwargs):
    if kwargs["created"]:
        calls = Call.objects.all()
    else:
        calls = instance.calls

    for call in calls:
        recategorize_call.delay(call.pk)
