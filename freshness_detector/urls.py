from django.urls import path
from . import views

urlpatterns = [
    path('', views.freshness_detector, name='freshness_detector'),
]