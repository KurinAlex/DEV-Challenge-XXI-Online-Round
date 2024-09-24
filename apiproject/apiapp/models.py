from django.db import models
from django.contrib.postgres.fields import ArrayField


class EmotionalTone(models.enums.TextChoices):
    NEUTRAL = 'NEU', 'Neutral'
    POSITIVE = 'POS', 'Positive'
    NEGATIVE = 'NEG', 'Negative'
    ANGRY = 'ANG', 'Angry'


class Category(models.Model):
    title = models.CharField()
    points = ArrayField(base_field=models.CharField(max_length=200), blank=True)


class Call(models.Model):
    name = models.CharField()
    location = models.CharField()
    emotional_tone = models.CharField(max_length=3, choices=EmotionalTone.choices, default=EmotionalTone.NEUTRAL)
    text = models.CharField()
    categories = models.ManyToManyField(Category)