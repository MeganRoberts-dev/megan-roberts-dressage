from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import Order, Booking
from services.models import Service
import stripe


@require_POST
def cache_checkout_data(request):
    """Handle Stripe client secret modification."""
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid)
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Error, please try again.')
        return HttpResponse(content=str(e), status=400)


def add_to_checkout(request, service_id):
    """Add selected service to the checkout session."""
    service = get_object_or_404(Service, id=service_id)
    if 'checkout_services' not in request.session:
        request.session['checkout_services'] = []

    if service_id not in request.session['checkout_services']:
        request.session['checkout_services'].append(service_id)

    request.session.modified = True
    return redirect('checkout')


def checkout(request, service_id):
    """Handle the checkout process, including creating Stripe payment intent."""
    service = get_object_or_404(Service, id=service_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'GET':
        # Create Stripe PaymentIntent for the service
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(service.price * 100),  # Convert price to cents
            currency=settings.STRIPE_CURRENCY,
        )

        context = {
            'service': service,
            'stripe_public_key': stripe_public_key,
            'stripe_secret_key': stripe_secret_key,
            'client_secret': intent.client_secret,
        }
        return render(request, 'checkout/checkout.html', context)

    if request.method == 'POST':
        # Extract POST data
        date = request.POST.get('date')
        time = request.POST.get('time')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')

        if not all([date, time, email]):
            messages.error(request, "Please fill in all the required fields, including email.")
            return redirect('checkout', service_id=service.id)

        # Create Order and Booking
        order = Order.objects.create(
            purchaser=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            total=service.price,
        )

        Booking.objects.create(
            order=order,
            service=service,
            date=date,
            time=time
        )

        return redirect(reverse('success', kwargs={'order_id': order.id}))


def success(request, order_id):
    """Render the success page and send the booking confirmation email."""
    order = get_object_or_404(Order, id=order_id)

    if order.email:
        try:
            subject = "Thank you for your booking with Megan Roberts Dressage"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [order.email]

            # Prepare the HTML content for the email
            html_content = render_to_string('checkout/booking-email.html', {
                'order': order,
                'bookings': order.bookings.all(),
            })

            send_mail(
                subject,
                '',
                from_email,
                to_email,
                html_message=html_content
            )

        except Exception as e:
            print(f"Failed to send email: {e}")

    context = {'order': order}
    return render(request, 'checkout/success.html', context)


def delete_service(request, service_id):
    """Remove a service from the checkout session (NOT from the database)."""
    if request.method == "POST":

        service = get_object_or_404(Service, id=service_id)

        if 'checkout_services' in request.session:
            checkout_services = request.session['checkout_services']
    
            if service_id in checkout_services:
                checkout_services.remove(service_id)
                request.session['checkout_services'] = checkout_services
                request.session.modified = True

                messages.success(request, f"Service '{service.name}' has been removed from your checkout.")

        else:
            messages.error(request, "No services in the checkout session.")

    return redirect('services')
