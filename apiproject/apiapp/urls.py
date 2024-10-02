"""
Web API URLs.
"""

from django.urls import path
from .views import *

urlpatterns = [
    path("category", CategoryListCreateAPIView.as_view()),
    path("category/<pk>", CategoryUpdateDestroyAPIView.as_view()),
    path("call/<pk>", CallRetrieveAPIView.as_view()),
    path("call", CallCreateAPIView.as_view()),
]
