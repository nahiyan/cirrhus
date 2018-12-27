from django.urls import path
from . import views

app_name = 'snapshots'

urlpatterns = [
    path('<str:snapshot_id>', views.detail, name = 'detail'),
    path('delete/<str:snapshot_id>', views.delete, name = 'delete'),
]