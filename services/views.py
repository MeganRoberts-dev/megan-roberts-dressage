from django.shortcuts import render
from .models import Service


def services(request):
    services = Services.objects.all().order_by('price')
    template = 'services/services.html'
    context = {
        'services': services,
    }
    return render(request, template, context)

