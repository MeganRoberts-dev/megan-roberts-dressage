# In services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name='services'),
    path('add/', views.add_service, name='add_service'),
    path('edit/<int:id>/', views.edit_service, name='edit_service'),
    path('delete/<int:id>/', views.delete_service, name='delete_service'),
]
