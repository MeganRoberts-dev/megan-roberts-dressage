from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from services.models import Service
from .models import Order, Booking
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        purchaser = request.user
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not all([date, time]):
            messages.error(request, "Please fill in all the fields.")
            return redirect('checkout', service_id=service.id)

        order = Order.objects.create(
            purchaser=purchaser,
            total=service.price,
        )

        Booking.objects.create(
            order=order,
            service=service,
            date=date,
            time=time
        )

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(service.price * 100),
                currency='usd',
                metadata={'order_id': order.id},
            )

            stripe_public_key = settings.STRIPE_PUBLIC_KEY
            client_secret = intent.client_secret

            context = {
                'order_form': order,
                'stripe_public_key': stripe_public_key,
                'client_secret': client_secret,
                'service': service
            }

            template = 'checkout/checkout.html'
            return render(request, template, context)

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment error: {e.user_message}")
            return redirect('checkout', service_id=service.id)

    return render(request, 'checkout.html', {'service': service})

def success(request):
    return render(request, 'success.html')
