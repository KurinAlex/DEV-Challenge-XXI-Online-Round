from django.urls import path
from .views import *

urlpatterns = [
    path('categories', CategoryListAPIView.as_view()),
    path('categories/<int:pk>', CategoryDetailAPIView.as_view()),
]
