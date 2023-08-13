from django.urls import path

from . import views

urlpatterns = [
    path('saved', views.index, name='index')
]
