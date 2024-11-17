from django.contrib import admin
from django.urls import path
from mailsender import views

urlpatterns = [
   path('send_mail/', views.send_mail, name="send_mail"),
]