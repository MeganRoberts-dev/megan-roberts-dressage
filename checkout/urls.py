from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:service_id>/', views.checkout, name='checkout'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('', views.success, name='booking-email'),
]
