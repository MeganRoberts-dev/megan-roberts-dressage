from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Booking, Order


@login_required
def profile(request):
    """
    Retrieve the user's profile.
    """
    user = User.objects.get(username=request.user.username)
    profile = UserProfile.objects.get(user=request.user)

    # retrieve the user's previous bookings
    bookings = Booking.objects.filter(order__purchaser=request.user)

    # retrieve profile
    form = UserProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            messages.success(request, 'Profile successfully updated!')
        else:
            messages.error(request, 'Error: Please try again')

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'form': form,
        'bookings': bookings,
    }
    return render(request, template, context)
