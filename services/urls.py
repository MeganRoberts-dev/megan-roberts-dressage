from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name='services'),
    path('add/', views.add_service, name='add_service'),
    path('edit/<int:id>/', views.edit_service, name='edit_service'),
    path(
        'delete_service_admin/<int:id>/',
        views.delete_service_admin,
        name='delete_service_admin'),
]
