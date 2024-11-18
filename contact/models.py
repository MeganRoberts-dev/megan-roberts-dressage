from django.db import models


class Contact(models.Model):
    """ Contact form fields """
    first_name = models.CharField(max_length=75, blank=False, null=False)
    last_name = models.CharField(max_length=75, blank=False, null=False)
    email = models.EmailField(max_length=256, blank=False, null=False)
    comments = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return self.email
