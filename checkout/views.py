from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from .models import Order, Booking
from services.models import Service
import stripe


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid)
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'error, please try again')
        return HttpResponse(content=e, status=400)
        

def add_to_checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if 'checkout_services' not in request.session:
        request.session['checkout_services'] = []

    # Add the service to the checkout if not already there
    if service_id not in request.session['checkout_services']:
        request.session['checkout_services'].append(service_id)

    request.session.modified = True
    return redirect('checkout')


def checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Handle GET request to display the checkout page
    if request.method == 'GET':
        # Create a Stripe PaymentIntent
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(service.price * 100),
            currency=settings.STRIPE_CURRENCY,
        )

        # Get Stripe keys for client-side
        client_secret = intent.client_secret

        context = {
            'service': service,
            'stripe_public_key': stripe_public_key,
            'stripe_secret_key': stripe_secret_key,
            'client_secret': intent.client_secret,
        }
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

        return redirect(reverse('success', kwargs={'order_id': order.id}))

        # try:
        #     # Create a Stripe PaymentIntent
        #     intent = stripe.PaymentIntent.create(
        #         amount=int(service.price * 100),
        #         currency=settings.STRIPE_CURRENCY,
        #         metadata={'order_id': order.id},
        #     )

        #     # Get Stripe keys for client-side
        #     client_secret = intent.client_secret

        #     # Pass the necessary data to the success page
        #     context = {
        #         'order': order,
        #         'service': service,
        #         'stripe_public_key': stripe_public_key,
        #         'client_secret': client_secret,
        #         'date': date,
        #         'time': time,
        #     }

        #     # Return the checkout page with payment details
        #     return render(request, 'checkout/checkout.html', context)

        # except stripe.error.StripeError as e:
        #     # Handle Stripe errors
        #     messages.error(request, f"Payment error: {e.user_message}")
        #     return render(request, 'checkout/checkout.html', {'service': service})


    # # Redirect to success page if the form indicates successful payment
    # if request.method == 'POST' and 'payment_success' in request.POST:
    #     return redirect('success')


def success(request, order_id):
    """Display the success page after payment"""
    order_number = get_object_or_404(Order, id=order_id)
    
    # Display order details on success page
    context = {
        'order_number': order_number,
    }

    return render(request, 'checkout/success.html', context)

def delete_service(request, service_id):
    if request.method == "POST":
        # Ensure the service exists
        get_object_or_404(Service, id=service_id)

        # Check if the service is in the user's session (checkout)
        if 'checkout_services' in request.session:
            checkout_services = request.session['checkout_services']
            if service_id in checkout_services:
                checkout_services.remove(service_id)
                request.session['checkout_services'] = checkout_services
                request.session.modified = True

        # Redirect back to the services page
        return redirect('services')