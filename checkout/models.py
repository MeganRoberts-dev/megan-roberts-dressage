from django.db import models
from services.models import Service
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='checkout_order', null=False, blank=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    slot = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        # Calculate line_total based on service price and quantity
        self.line_total = self.service.price * self.quantity
        super().save(*args, **kwargs)
