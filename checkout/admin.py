from django.contrib import admin
from .models import Order, Booking


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("full_name", "purchaser", "email", "total", "created_at")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ["service"]
    list_display = ("order", "service", "date", "time")
