from django.test import TestCase
from django.urls import reverse
from checkout.forms import CheckoutForm
from checkout.models import Order, Booking
from services.models import Service
from unittest.mock import patch

class CheckoutFormTests(TestCase):
    def test_checkout_form_valid_data(self):
        form = CheckoutForm(data={
            'full_name': 'Megan Roberts',
            'email': 'megan@example.com',
        })
        self.assertTrue(form.is_valid())

    def test_checkout_form_missing_fields(self):
        form = CheckoutForm(data={
            'email': 'megan@example.com'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)

class CheckoutViewTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name="Test Service", price=25)

    @patch('checkout.views.stripe.PaymentIntent.create')
    def test_checkout_view_loads(self, mock_create_intent):
        mock_create_intent.return_value = {'client_secret': 'test_secret'}
        response = self.client.get(reverse('checkout', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
