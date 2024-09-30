from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ["id", "name", "location", "text", "emotional_tone", "categories"]

    emotional_tone = serializers.CharField(source="get_emotional_tone_display")
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return obj.categories.values_list("title", flat=True)


class AudioRequestSerializer(serializers.Serializer):
    audio_url = serializers.URLField(required=True)

    def validate_audio_url(self, value):
        if not value.endswith((".mp3", ".wav")):
            raise serializers.ValidationError("The URL must point to .mp3 or .wav audio file.")

        return value
