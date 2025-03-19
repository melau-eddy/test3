from django.contrib import admin
from .models import Bus, Route, Schedule, Booking, Payment

# Bus Admin
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_name', 'bus_number', 'total_seats', 'amenities')
    list_filter = ('bus_name', 'bus_number')
    search_fields = ('bus_name', 'bus_number')


# Route Admin
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination')
    list_filter = ('source', 'destination')
    search_fields = ('source', 'destination')


# Schedule Admin
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('bus', 'route', 'departure_time', 'arrival_time', 'price', 'available_seats')
    list_filter = ('bus', 'route', 'departure_time')
    search_fields = ('bus__bus_name', 'route__source', 'route__destination')


# Booking Admin
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'seats_booked', 'total_price', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'schedule__bus', 'schedule__route')
    search_fields = ('user__username', 'schedule__bus__bus_name', 'schedule__route__source', 'schedule__route__destination')


# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'payment_method', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('booking__user__username', 'transaction_id')