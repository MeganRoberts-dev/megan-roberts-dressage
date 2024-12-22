from django.urls import path
from . import views

urlpatterns = [
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('checkout/<int:service_id>/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]
