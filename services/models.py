from django.db import models
from cloudinary.models import CloudinaryField


class Service(models.Model):
    """Services being offered at Megan Roberts Dressage"""
    name = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField()
    price = models.PositiveIntegerField(null=False, blank=False)
    duration = models.CharField(max_length=100, null=False, blank=False)
    image = CloudinaryField(
        "image", default='placeholder',
        null=True, blank=True)

    def __str__(self):
        return self.name
