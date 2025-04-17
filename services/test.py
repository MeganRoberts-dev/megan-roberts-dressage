from django.test import TestCase
from .models import Service
from .forms import ServiceForm


class ServiceModelFormTests(TestCase):

    def test_service_model_creation(self):
        service = Service.objects.create(
            name="Private Lesson",
            description="One-on-one dressage lesson.",
            price=50,
            duration="1 hour",
            image="sample_image"
        )
        self.assertEqual(service.name, "Private Lesson")
        self.assertEqual(str(service), "Private Lesson")
        self.assertEqual(service.price, 50)
        self.assertEqual(service.duration, "1 hour")

    def test_service_form_valid_data(self):
        form_data = {
            'name': 'Group Lesson',
            'description': 'Group session for up to 4 riders.',
            'price': 35,
            'duration': '1 hour',
            'image': 'sample_image'
        }
        form = ServiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_service_form_missing_required_fields(self):
        form_data = {
            'name': '',
            'description': '',
            'price': '',
            'duration': '',
            'image': ''
        }
        form = ServiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('duration', form.errors)

    def test_service_form_negative_price_invalid(self):
        form_data = {
            'name': 'Faulty Service',
            'description': 'Invalid price test',
            'price': -10,
            'duration': '30 minutes',
            'image': 'sample_image'
        }
        form = ServiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
