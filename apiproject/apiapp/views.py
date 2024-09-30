from django.shortcuts import get_object_or_404

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from celery import uuid
from celery.result import AsyncResult

from .models import *
from .serializers import *
from .tasks import process_file


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


class CallRetrieveAPIView(APIView):

    def get(self, request, pk):
        call = get_object_or_404(Call, pk=pk)
        result = AsyncResult(call.task_id)

        if result.ready():
            serializer = CallSerializer(call)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_202_ACCEPTED)


class CallCreateAPIView(APIView):

    def post(self, request):
        input_serializer = AudioRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        audio_url = input_serializer.validated_data["audio_url"]

        task_id = uuid()
        call = Call.objects.create(task_id=task_id)

        process_file.apply_async((call.pk, audio_url), task_id=task_id)

        return Response({"id": call.pk})
