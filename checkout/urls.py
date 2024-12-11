from django.urls import path
from . import views
from services.views import service_list

urlpatterns = [
    path('checkout/<int:service_id>/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('services/', service_list, name='service_list'),
]
