from django.urls import path

from . import views

urlpatterns = [
    path('saved', views.index, name='index')
]
# format: path('the name of the page that goes after the link', views.index, name='index')
# different names after / leads to different paths
# it then shows index from views
