from django.urls import include, path
from . import views
from django.contrib import admin
from rest_framework import routers
router = routers.DefaultRouter()
urlpatterns = [
    path('image', views.process_image)
]