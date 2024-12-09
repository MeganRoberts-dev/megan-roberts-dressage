from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:service_id>/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]