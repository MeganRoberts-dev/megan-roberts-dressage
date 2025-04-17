from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm


class UserProfileModelFormTests(TestCase):

    def test_user_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='testuser', password='password123')
        # The signal should create the profile automatically
        profile = UserProfile.objects.get(user=user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user.username, 'testuser')

    def test_user_profile_str_representation(self):
        user = User.objects.create_user(username='janedoe', password='securepass')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(str(profile), 'janedoe')

    def test_user_profile_form_valid_data(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe'
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_missing_data(self):
        form_data = {
            'first_name': '',
            'last_name': ''
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_user_profile_form_partial_invalid_data(self):
        form_data = {
            'first_name': 'Alice',
            'last_name': ''
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
