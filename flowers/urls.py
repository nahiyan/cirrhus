from django.urls import path
from . import views

app_name = 'flowers'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('run', views.run, name = 'run'),
    path('generate_training_data/<int:training_data_id>/', views.generate_training_data, name = 'generate_training_data'),
    path('generate_input_data/<int:input_data_id>/', views.generate_input_data, name = 'generate_input_data'),
    path('initialize_training_session/<int:training_session_id>', views.initialize_training_session, name = 'initialize_training_session'),
    path('input_data_detail/<int:input_data_id>', views.input_data_detail, name = 'input_data_detail'),
    path('train/<int:training_session_id>', views.train, name = 'train'),
]