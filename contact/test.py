from django.test import TestCase
from .models import Contact
from .forms import ContactForm


class ContactModelFormTests(TestCase):

    def test_contact_model_creation(self):
        contact = Contact.objects.create(
            first_name='Alice',
            last_name='Smith',
            email='alice@example.com',
            comments='This is a test comment.'
        )
        self.assertEqual(str(contact), 'alice@example.com')
        self.assertEqual(contact.first_name, 'Alice')
        self.assertIsNotNone(contact.date)

    def test_contact_form_valid_data(self):
        form_data = {
            'first_name': 'Bob',
            'last_name': 'Brown',
            'email': 'bob@example.com',
            'comments': 'This is a sample message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid_missing_fields(self):
        form_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'comments': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('comments', form.errors)

    def test_contact_form_invalid_email(self):
        form_data = {
            'first_name': 'Charlie',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'comments': 'Message with bad email.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
