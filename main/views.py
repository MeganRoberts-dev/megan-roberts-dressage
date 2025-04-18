from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user(request):
    logout(request)
    return redirect('/')
from django.contrib.auth import logout
from django.shortcuts import render, redirect


def logout_user(request):
    """ Logout User """
    logout(request)
    return redirect('/')


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "404.html", status=404)