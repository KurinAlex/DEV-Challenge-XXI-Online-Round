from django.urls import path
from .views import *

urlpatterns = [
    path("category", CategoryListAPIView.as_view()),
    path("category/<int:pk>", CategoryDetailAPIView.as_view()),
    path("call/<int:pk>", CallGetAPIView.as_view()),
    path("call", CallPostAPIView.as_view()),
]
