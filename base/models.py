from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Bus Model
class Bus(models.Model):
    bus_name = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=20, unique=True)
    total_seats = models.PositiveIntegerField(default=40)
    amenities = models.TextField(blank=True, null=True)  # e.g., WiFi, AC, Charging Ports
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return f"{self.bus_name} ({self.bus_number})"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


# Route Model
class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    # distance = models.PositiveIntegerField(help_text="Distance in kilometers")
    # duration = models.DurationField(help_text="Duration of the journey")

    def __str__(self):
        return f"{self.source} to {self.destination}"


# Schedule Model
class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='schedules')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_seats = models.PositiveIntegerField(default=40)

    def __str__(self):
        return f"{self.bus.bus_name} - {self.route.source} to {self.route.destination} at {self.departure_time}"


# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='bookings')
    seats_booked = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Booking #{self.id} by {self.user.username} for {self.schedule}"


# Payment Model
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NETBANKING', 'Net Banking'),
    )
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Payment #{self.id} for Booking #{self.booking.id}"