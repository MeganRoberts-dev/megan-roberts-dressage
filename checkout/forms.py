from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full Name'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email Address'}
            ),
        }

