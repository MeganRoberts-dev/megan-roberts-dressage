from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse ("This is my homepage (/)")
