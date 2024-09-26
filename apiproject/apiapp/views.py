import time
import threading
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *


class CategoryListAPIView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response()


processing_status = {}


class CallGetAPIView(APIView):

    def get_object(self, pk):
        try:
            return Call.objects.get(pk=pk)
        except Call.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        call = self.get_object(pk=pk)
        if pk not in processing_status:
            raise Http404

        status_info = processing_status[pk]
        if status_info["status"] == "processing":
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            serializer = CallSerializer(call)
            return Response(serializer.data)


class CallPostAPIView(APIView):

    def process_file(file_url, id):
        time.sleep(10)
        processing_status[id] = {"status": "completed", "result": "File processed successfully!"}

    def post(self, request):
        input_serializer = AudioRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        audio_url = input_serializer.validated_data["audio_url"]

        call = Call.objects.create()
        id = call.pk
        processing_status[id] = {"status": "processing"}

        thread = threading.Thread(target=CallPostAPIView.process_file, args=(audio_url, id))
        thread.start()

        call = Call.objects.create()
        return Response({"id": id})
