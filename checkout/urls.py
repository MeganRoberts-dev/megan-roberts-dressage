from django.urls import path
from . import views
from services.models import Service

urlpatterns = [
    path('checkout/<int:service_id>/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]