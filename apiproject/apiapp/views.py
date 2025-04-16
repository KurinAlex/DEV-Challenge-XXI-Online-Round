"""
Web API controllers (Django views)
"""

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import *
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


class CallRetrieveAPIView(APIView):

    def get(self, request, pk):
        call = get_call_if_processed(pk)
        if call is None:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            serializer = CallSerializer(call)
            return Response(serializer.data)


class CallCreateAPIView(APIView):

    def post(self, request):
        input_serializer = AudioRequestSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        audio_url = input_serializer.validated_data["audio_url"]

        call_id = post_call(audio_url)

        return Response({"id": call_id})
