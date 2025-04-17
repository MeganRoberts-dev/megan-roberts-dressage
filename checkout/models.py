from django.db import models
from django.contrib.auth.models import User

from services.models import Service


class Order(models.Model):
    purchaser = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    full_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )  # Optional full name for guest users
    email = models.EmailField(
        null=True,
        blank=True
    )  # Optional email for guest users
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.purchaser.email}"


class Booking(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return (
            f"Booking for {self.service.name} on {self.date} at {self.time}"
        )