from django.urls import path
from . import views

app_name = 'input_data'

urlpatterns = [
    path('<str:flavor_machine_name>', views.list, name = 'list'),
    path('create/<str:flavor_machine_name>', views.create, name = 'create'),
    path('delete/<int:input_data_id>', views.delete, name = 'delete'),
]