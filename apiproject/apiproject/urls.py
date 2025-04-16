"""
Application URL configuration.
"""

from django.urls import path, include

urlpatterns = [
    path("api/", include("apiapp.urls")),
]
