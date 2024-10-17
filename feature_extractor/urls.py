from django.urls import path
from . import views

urlpatterns = [
    path('', views.feature_extractor, name='feature_extractor'),
]