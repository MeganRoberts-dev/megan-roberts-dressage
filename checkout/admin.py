from django.contrib import admin
from .models import Order, Booking


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "created_at", "total")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("date", "time")
