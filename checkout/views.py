import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from bag.models import OrderItem

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    order_items = OrderItem.objects.filter(order__user=request.user)
    total_price = sum(item.line_total for item in order_items)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.service.name,
                    },
                    'unit_amount': int(item.line_total * 100),
                },
                'quantity': item.quantity,
            }
            for item in order_items
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return redirect(session.url, code=303)

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
