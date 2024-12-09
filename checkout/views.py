from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from services.models import Service
from .models import Order, OrderItem
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    # Handle POST request when user submits the form
    if request.method == 'POST':
        # Retrieve slot, date, and time from the POST request
        slot = request.POST.get('slot')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Validate that slot, date, and time are provided
        if not slot or not date or not time:
            messages.error(request, "Please select a valid slot, date, and time.")
            return redirect('checkout', service_id=service.id)

        # Create an order without requiring user authentication
        order = Order.objects.create(
            full_name=request.POST.get('full_name', 'Guest'),  # Default to 'Guest' if no name provided
            email=request.POST.get('email', 'guest@example.com'),  # Default to 'guest@example.com' if no email
            total=service.price,
        )

        # Create an order item with selected slot, date, and time
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

            # Redirect to Stripe Checkout
            return redirect(session.url, code=303)

        except stripe.error.StripeError as e:
            messages.error(request, f"Payment error: {e.user_message}")
            return redirect('checkout', service_id=service.id)

    else:
        # GET request when the page is first loaded
        return render(request, 'checkout.html', {'service': service})

# Success page
def success(request):
    return render(request, 'checkout/success.html')

# Cancel page
def cancel(request):
    return render(request, 'checkout/cancel.html')
