from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Service
from .forms import ServiceForm


def services(request):
    services = Service.objects.all().order_by('price')
    template = 'services/services.html'
    context = {
        'services': services,
    }
    return render(request, template, context)


@login_required
def add_service(request):
    """Add new service as superuser"""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: Invalid credentials")
        return redirect("home")

    if request.method == "POST":
        service_form = ServiceForm(request.POST or None, request.FILES)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, "Service Added!")
            return redirect('services')

        messages.error(request, "Error: Please try again")

    service_form = ServiceForm(request.POST or None)
    template = 'services/add-service.html'
    context = {
        'service_form': service_form,
    }
    return render(request, template, context)


@login_required
def edit_service(request, id):
    """Edit an existing service as superuser"""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: Invalid credentials")
        return redirect("home")

    service = get_object_or_404(Service, id=id)
    service_form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST":
        if service_form.is_valid():
            service_form.save()
            messages.success(request, "Service Updated!")
            return redirect('services')

        messages.error(request, "Error: Please try again")

    template = 'services/edit-service.html'
    context = {
        'service': service,
        'service_form': service_form,
    }
    return render(request, template, context)


@login_required
def delete_service_admin(request, id):
    """Delete a service from the database (only accessible by superuser)"""
    if not request.user.is_superuser:
        messages.error(request, "Access denied: Invalid credentials")
        return redirect("home")

    service = get_object_or_404(Service, id=id)
    # Delete the service from the database
    service.delete()

    messages.success(request, f"Service '{service.name}' has been deleted.")
    return redirect('services')
