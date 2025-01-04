from django.urls import path

from . import views

urlpatterns = [
    path("userLocation", views.getCurrentLocation, name="getLocation")
]