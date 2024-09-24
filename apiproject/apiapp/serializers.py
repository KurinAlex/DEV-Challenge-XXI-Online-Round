from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
        
class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'