from django.urls import path
from . import views

urlpatterns = [
    path('', views.object_detection, name='object_detection'),

]