from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any extra fields here, e.g. phone number or avatar

    def __str__(self):
        return self.user.username
