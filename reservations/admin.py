from django.contrib import admin
from .models import Airport, Flight, Booking, Passenger

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city', 'country')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline_name', 'origin', 'destination', 'departure_time', 'status')
    list_filter = ('status', 'origin', 'destination', 'airline_name')
    search_fields = ('flight_number', 'airline_name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'user', 'flight', 'status', 'booked_at')
    list_filter = ('status', 'seat_class')
    search_fields = ('booking_ref', 'user__username', 'flight__flight_number')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking', 'seat_number')
    search_fields = ('first_name', 'last_name', 'booking__booking_ref', 'passport_number')

