from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('', views.contact, name='email-confirm'),
]
