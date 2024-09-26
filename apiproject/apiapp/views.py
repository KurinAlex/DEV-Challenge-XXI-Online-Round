import time
import threading
from django.http import Http404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryUpdateDestroyAPIView(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response


processing_status = {}


class CallRetrieveAPIView(APIView):

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


class CallCreateAPIView(APIView):

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

        thread = threading.Thread(target=CallCreateAPIView.process_file, args=(audio_url, id))
        thread.start()

        call = Call.objects.create()
        return Response({"id": id})
