"""
URL configuration for apiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('apiapp.urls')),
]
