"""
Application database models.
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField


class EmotionalTone(models.IntegerChoices):
    NEUTRAL = 0, "Neutral"
    POSITIVE = 1, "Positive"
    NEGATIVE = 2, "Negative"
    ANGRY = 3, "Angry"


class Category(models.Model):
    title = models.CharField(unique=True)
    points = ArrayField(base_field=models.CharField(), blank=True)


class Call(models.Model):
    name = models.CharField(null=True)
    location = models.CharField(null=True)
    emotional_tone = models.IntegerField(choices=EmotionalTone.choices, null=True)
    text = models.CharField(null=True)
    categories = models.ManyToManyField(Category, related_name="calls")
    task_id = models.CharField(null=True)
