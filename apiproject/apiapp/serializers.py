from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = "__all__"

    emotional_tone = serializers.CharField(source="get_emotional_tone_display")
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return obj.categories.values_list("title", flat=True)


class AudioRequestSerializer(serializers.Serializer):
    audio_url = serializers.URLField(required=True)

    def validate_audio_url(self, value):
        # You can add custom validation logic here if needed, e.g., check file type.
        if not value.endswith((".mp3", ".wav")):
            raise serializers.ValidationError("The audio URL must point to a valid audio file (e.g., .mp3, .wav).")

        return value
