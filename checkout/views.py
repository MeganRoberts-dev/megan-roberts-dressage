from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Service, Order, Booking
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY


def service_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not all([full_name, email, date, time]):
            messages.error(request, "Please fill in all the fields.")
            return redirect('checkout', service_id=service.id)

        # Create order and booking
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            total=service.price,
        )
        Booking.objects.create(order=order, service=service, date=date, time=time)

        try:
            # Create a payment intent with Stripe (for the checkout session)
            intent = stripe.PaymentIntent.create(
                amount=int(service.price * 100),  # Stripe expects amount in cents
                currency='usd',
                metadata={'order_id': order.id},
            )

            stripe_public_key = settings.STRIPE_PUBLIC_KEY
            client_secret = intent.client_secret

            # Pass the order form, Stripe keys, and client secret to the template context
            context = {
                'order_form': order,
                'stripe_public_key': stripe_public_key,
                'client_secret': client_secret,
                'service': service
            }

            # Render the checkout page with the required context
            template = 'checkout/checkout.html'
            return render(request, template, context)

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment error: {e.user_message}")
            return redirect('checkout', service_id=service.id)

    return render(request, 'checkout.html', {'service': service})

def success(request):
    return render(request, 'success.html')
