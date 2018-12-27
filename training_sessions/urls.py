from django.urls import path
from . import views

app_name = 'training_sessions'

urlpatterns = [
    path('create/<str:flavor_machine_name>', views.create, name = 'create'),
    path('<int:training_session_id>', views.detail, name = 'detail'),
    path('<str:flavor_machine_name>', views.list, name = 'list'),
    path('run/<int:training_session_id>', views.run, name = 'run'),
    path('delete/<int:training_session_id>', views.delete, name = 'delete'),
]