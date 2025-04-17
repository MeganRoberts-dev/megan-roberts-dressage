from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time

from .models import Order, Booking
from services.models import Service  # Ensure this import path is correct
from .forms import CheckoutForm


class OrderBookingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.service = Service.objects.create(
            name='Test Service',
            description='Service description',
            price=100.00
        )

    def test_order_creation(self):
        order = Order.objects.create(
            purchaser=self.user,
            full_name='John Doe',
            email='john@example.com',
            total=100.00
        )
        self.assertEqual(order.__str__(), f"Order #{order.id} - john@example.com")
        self.assertEqual(order.purchaser.username, 'testuser')

    def test_booking_creation(self):
        order = Order.objects.create(
            purchaser=self.user,
            full_name='John Doe',
            email='john@example.com',
            total=100.00
        )
        booking = Booking.objects.create(
            order=order,
            service=self.service,
            date=date.today(),
            time=time(14, 30)
        )
        expected_str = f"Booking for {self.service.name} on {booking.date} at {booking.time}"
        self.assertEqual(str(booking), expected_str)
        self.assertEqual(booking.order, order)

    def test_checkout_form_valid_data(self):
        form_data = {
            'full_name': 'Jane Doe',
            'email': 'jane@example.com'
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_checkout_form_invalid_data(self):
        form_data = {
            'full_name': '',
            'email': 'not-an-email'
        }
        form = CheckoutForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('email', form.errors)
