from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from services.models import Service
from django.contrib.auth.models import User

# View the current shopping bag
def view_bag(request):
    if request.user.is_authenticated:
        # Get the user's order (if exists) or create one if it doesn't
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        order_items = order.items.all()
        total_price = sum(item.line_total for item in order_items)
    else:
        order_items = []
        total_price = 0

    return render(request, 'bag/bag.html', {
        'order_items': order_items,
        'total_price': total_price,
    })

# Add a service to the shopping bag
def add_to_bag(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    quantity = request.POST.get('quantity', 1)  # Default quantity is 1

    # Check if the user already has an order
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
    else:
        order, created = Order.objects.get_or_create(user=None, completed=False)

    # Create or update the order item
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        service=service,
        defaults={'quantity': quantity, 'line_total': service.price * int(quantity)}
    )
    if not created:
        # If the item already exists, update the quantity and line_total
        order_item.quantity += int(quantity)
        order_item.line_total = order_item.quantity * service.price
        order_item.save()

    return redirect('view_bag')

# Adjust the quantity of an item in the bag (cart)
def adjust_bag(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    quantity = request.POST.get('quantity', 1)

    if request.user.is_authenticated:
        order = Order.objects.get(user=request.user, completed=False)
        order_item = OrderItem.objects.get(order=order, service=service)
        order_item.quantity = int(quantity)
        order_item.line_total = order_item.quantity * service.price
        order_item.save()

    return redirect('view_bag')

# Remove an item from the bag (cart)
def remove_from_bag(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.user.is_authenticated:
        order = Order.objects.get(user=request.user, completed=False)
        order_item = OrderItem.objects.get(order=order, service=service)
        order_item.delete()

    return redirect('view_bag')
