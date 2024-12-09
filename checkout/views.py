from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from services.models import Service
from .models import Order, OrderItem
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request, service_id):
    service = get_service_by_id(service_id)  
    return render(request, 'checkout.html', {'service': service})
    
    # Check if the user has selected a slot, if not show an error
    slot = request.POST.get('slot', None)
    date = request.POST.get('date', None)
    time = request.POST.get('time', None)
    
    if not slot or not date or not time:
        messages.error(request, "Please select a valid slot, date, and time.")
        return redirect('services')  # Redirect back to the services page if no slot is selected

    # Create an order
    order = Order.objects.create(
        user=request.user,
        full_name=request.user.get_full_name(),
        email=request.user.email,
        total=service.price,
    )

    # Create order item with selected slot, date, and time
    OrderItem.objects.create(
        order=order,
        service=service,
        slot=slot,
        date=date,
        time=time,
        quantity=1,
    )

    try:
        # Create Stripe session for payment
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'gbp',  # Correct currency code for GBP
                        'product_data': {
                            'name': service.name,
                        },
                        'unit_amount': int(service.price * 100),  # Convert price to cents
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        return redirect(session.url, code=303)

    except stripe.error.StripeError as e:
        messages.error(request, f"Payment error: {e.user_message}")
        return redirect('checkout')  # Redirect to checkout if there's an error

def success(request):
    return render(request, 'checkout/success.html')

def cancel(request):
    return render(request, 'checkout/cancel.html')    
