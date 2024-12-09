from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home or another page if already logged in
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            # Redirect to 'next' or home page
            next_url = request.GET.get('next', 'home')  
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You are now registered and logged in.")

            # Capture the service details from the query parameters
            service_id = request.GET.get('service_id')
            date = request.GET.get('date')
            time = request.GET.get('time')

            # If there are service details, redirect to the checkout page with them
            if service_id and date and time:
                return redirect('checkout', service_id=service_id, date=date, time=time)
            else:
                return redirect('home')  # Or another page if no service details are provided

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
