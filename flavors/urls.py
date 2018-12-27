from django.urls import path, include

from . import views

app_name = 'flavors'

urlpatterns = [
    path('', views.index, name='index')
]