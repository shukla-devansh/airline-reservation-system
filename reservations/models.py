from django.db import models
from django.contrib.auth.models import User
import uuid


class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.city}, {self.country}"


class Flight(models.Model):
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departing_flights')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arriving_flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField(default=180)
    available_seats = models.IntegerField(default=180)
    economy_price = models.DecimalField(max_digits=10, decimal_places=2)
    business_price = models.DecimalField(max_digits=10, decimal_places=2)
    first_class_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    airline_name = models.CharField(max_length=100, default='SkyWave Airlines')

    def duration(self):
        delta = self.arrival_time - self.departure_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"

    def __str__(self):
        return f"{self.flight_number}: {self.origin.code} → {self.destination.code}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    CLASS_CHOICES = [
        ('economy', 'Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    booking_ref = models.CharField(max_length=8, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    seat_class = models.CharField(max_length=20, choices=CLASS_CHOICES, default='economy')
    passengers = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booked_at = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_ref} - {self.user.username}"


class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passenger_list')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField()
    seat_number = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
