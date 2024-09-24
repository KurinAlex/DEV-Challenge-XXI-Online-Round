from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from .models import *
from .serializers import *


class CategoryListAPIView(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CategoryDetailAPIView(APIView):
    parser_classes = (MultiPartParser, JSONParser)

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response()