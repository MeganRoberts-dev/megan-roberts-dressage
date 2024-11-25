from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    """
        Form to allow superusers to manage services.
    """

    class Meta:
        model = Service
        fields = "__all__"
