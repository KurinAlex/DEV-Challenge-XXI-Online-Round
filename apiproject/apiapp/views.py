import threading
import json
import wave
import vosk
import os
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from requests import get


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

    def get(self, request, pk):
        call = get_object_or_404(Call, pk=pk)
        if int(pk) not in processing_status:
            raise Http404

        status_info = processing_status[int(pk)]
        if status_info["status"] == "processing":
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            serializer = CallSerializer(call)
            return Response(serializer.data)


class CallCreateAPIView(APIView):

    def process_file(file, id):
        if os.path.exists(file):
            file_stream = open(file, "rb")
        else:
            response = get(file, stream=True)
            file_stream = response.raw

        with wave.open(file_stream) as wf:
            model = vosk.Model(lang="en-us")
            rec = vosk.KaldiRecognizer(model, wf.getframerate())

            while True:
                data = wf.readframes(wf.getframerate())
                if len(data) == 0:
                    break

                rec.AcceptWaveform(data)

        file_stream.close()

        call = get_object_or_404(Call, pk=id)
        text = json.loads(rec.FinalResult())["text"]

        call.text = text
        call.save()

        processing_status[id] = {"status": "completed"}

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
