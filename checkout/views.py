from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Order, Booking
from services.models import Service
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    # Handle GET request to display the checkout page
    if request.method == 'GET':
        context = {'service': service}
        return render(request, 'checkout/checkout.html', context)

    # Handle POST request to process the form submission
    if request.method == 'POST':
        # Allow anonymous users; purchaser will be None if not logged in
        purchaser = request.user if request.user.is_authenticated else None
        date = request.POST.get('date')
        time = request.POST.get('time')
        email = request.POST.get('email')  # Optional guest email field

        # Validate required fields
        if not all([date, time, email]):
            messages.error(request, "Please fill in all the required fields, including email.")
            return redirect('checkout', service_id=service.id)

        # Create Order
        full_name = request.POST.get('full_name', None)
        order = Order.objects.create(
            purchaser=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            total=service.price,
        )

        # Create Booking
        Booking.objects.create(
            order=order,
            service=service,
            date=date,
            time=time
        )

        try:
            # Create a Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(service.price * 100),
                currency='usd',
                metadata={'order_id': order.id},
            )

            # Get Stripe keys for client-side
            stripe_public_key = settings.STRIPE_PUBLIC_KEY
            client_secret = intent.client_secret

            # Pass the necessary data to the success page
            context = {
                'order': order,
                'service': service,
                'stripe_public_key': stripe_public_key,
                'client_secret': client_secret,
                'date': date,
                'time': time
            }

            # Return the checkout page with payment details
            return render(request, 'checkout/checkout.html', context)

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            messages.error(request, f"Payment error: {e.user_message}")
            return render(request, 'checkout/checkout.html', {'service': service})

    # Redirect to success page if the form indicates successful payment
    if request.method == 'POST' and 'payment_success' in request.POST:
        return redirect('success')


def success(request):
    """Display the success page after payment"""
    order_number = request.GET.get('order_number')  # Retrieve the order number if available
    date = request.GET.get('date')  # Retrieve the date chosen
    time = request.GET.get('time')  # Retrieve the time chosen
    total = request.GET.get('total')  # Retrieve the total amount

    # Display order details on success page
    context = {
        'order_number': order_number,
        'date': date,
        'time': time,
        'total': total,
    }

    return render(request, 'checkout/success.html', context)
