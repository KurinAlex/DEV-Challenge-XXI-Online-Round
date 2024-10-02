from django.test import TestCase

from rest_framework.exceptions import ValidationError

from .models import *
from .processing import *
from .serializers import *


class SerializersTestCase(TestCase):
    def test_wrong_audio_url_validates(self):
        for url in ["http://test.com/test.wav", "https://example.com/audio.mp3"]:
            serializer = AudioRequestSerializer(data={"audio_url": url})
            self.assertEqual(serializer.is_valid(), True)

    def test_wrong_audio_url_throws(self):
        for url in ["wrong/url", "https://example.com/audio.ogg"]:
            with self.assertRaises(ValidationError):
                serializer = AudioRequestSerializer(data={"audio_url": url})
                serializer.is_valid(raise_exception=True)


class TextProcessingTestCase(TestCase):
    def setUp(self):
        Category.objects.create(title="Passport", points=["Passport", "Visa"])
        Category.objects.create(title="Animals", points=["Cats", "Dogs"])
        Category.objects.create(title="Travelling", points=["Hotels", "Bars"])

    def test_animals_can_speak(self):
        text = (
            "Hi! My name is Lisa. I am from Toronto. I would like to know when my passport visa will be ready. Thanks!"
        )
        self.assertEqual(get_emotional_tone(text), EmotionalTone.NEUTRAL)
        self.assertEqual(get_name_and_location(text), ("lisa", "toronto"))

        categories = get_categories(text)
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].title, "Passport")
