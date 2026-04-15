from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime, date
from functools import wraps
from .models import Flight, Airport, Booking, Passenger
from .forms import FlightSearchForm, BookingForm, PassengerFormSet, RegisterForm, LoginForm


def superuser_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'Only admin superusers can access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    form = FlightSearchForm(initial={'trip_type': 'one_way', 'passengers': 1, 'seat_class': 'economy'})
    airports = Airport.objects.all().order_by('city')
    upcoming_flights = Flight.objects.filter(status='scheduled', departure_time__gte=datetime.now()).order_by('departure_time')[:6]
    return render(request, 'reservations/home.html', {
        'form': form, 'airports': airports, 'upcoming_flights': upcoming_flights
    })


def search_flights(request):
    if request.method == 'GET':
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            origin = form.cleaned_data['origin'].upper()
            destination = form.cleaned_data['destination'].upper()
            dep_date = form.cleaned_data['departure_date']
            passengers = form.cleaned_data['passengers']
            seat_class = form.cleaned_data['seat_class']

            flights = Flight.objects.filter(
                origin__code=origin,
                destination__code=destination,
                departure_time__date=dep_date,
                available_seats__gte=passengers,
                status__in=['scheduled', 'delayed']
            ).select_related('origin', 'destination').order_by('departure_time')

            return render(request, 'reservations/search_results.html', {
                'flights': flights, 'form': form, 'passengers': passengers,
                'seat_class': seat_class, 'origin': origin, 'destination': destination,
                'dep_date': dep_date,
            })
    return redirect('home')


@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seat_class = request.GET.get('seat_class', 'economy')
    passengers_count = int(request.GET.get('passengers', 1))

    price_map = {'economy': flight.economy_price, 'business': flight.business_price, 'first': flight.first_class_price}
    price_per_person = price_map.get(seat_class, flight.economy_price)
    total = price_per_person * passengers_count

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        formset = PassengerFormSet(request.POST, initial=[{}] * passengers_count)
        if booking_form.is_valid() and formset.is_valid():
            booking = Booking.objects.create(
                user=request.user,
                flight=flight,
                seat_class=seat_class,
                passengers=passengers_count,
                total_price=total,
                contact_email=booking_form.cleaned_data['contact_email'],
                contact_phone=booking_form.cleaned_data.get('contact_phone', ''),
                status='confirmed'
            )
            for f in formset:
                if f.cleaned_data:
                    Passenger.objects.create(
                        booking=booking,
                        first_name=f.cleaned_data['first_name'],
                        last_name=f.cleaned_data['last_name'],
                        date_of_birth=f.cleaned_data['date_of_birth'],
                        passport_number=f.cleaned_data.get('passport_number', '')
                    )
            flight.available_seats -= passengers_count
            flight.save()
            messages.success(request, f'Booking confirmed! Reference: {booking.booking_ref}')
            return redirect('booking_confirmation', booking_ref=booking.booking_ref)
    else:
        booking_form = BookingForm(initial={'contact_email': request.user.email})
        formset = PassengerFormSet(initial=[{}] * passengers_count)

    return render(request, 'reservations/book_flight.html', {
        'flight': flight, 'booking_form': booking_form, 'formset': formset,
        'seat_class': seat_class, 'passengers_count': passengers_count,
        'price_per_person': price_per_person, 'total': total,
    })


@login_required
def booking_confirmation(request, booking_ref):
    booking = get_object_or_404(Booking, booking_ref=booking_ref, user=request.user)
    return render(request, 'reservations/booking_confirmation.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('flight__origin', 'flight__destination').order_by('-booked_at')
    return render(request, 'reservations/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_ref):
    booking = get_object_or_404(Booking, booking_ref=booking_ref, user=request.user)
    if booking.status == 'confirmed':
        booking.status = 'cancelled'
        booking.save()
        booking.flight.available_seats += booking.passengers
        booking.flight.save()
        messages.success(request, 'Booking cancelled successfully.')
    return redirect('my_bookings')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome aboard, {user.first_name}!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'reservations/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_superuser else 'home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()
    return render(request, 'reservations/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@superuser_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_airports = Airport.objects.count()
    total_flights = Flight.objects.count()
    total_bookings = Booking.objects.count()

    recent_users = User.objects.order_by('-date_joined')[:6]
    recent_flights = Flight.objects.select_related('origin', 'destination').order_by('-departure_time')[:6]
    recent_bookings = Booking.objects.select_related('user', 'flight__origin', 'flight__destination').order_by('-booked_at')[:8]

    return render(request, 'reservations/admin_dashboard.html', {
        'total_users': total_users,
        'total_airports': total_airports,
        'total_flights': total_flights,
        'total_bookings': total_bookings,
        'recent_users': recent_users,
        'recent_flights': recent_flights,
        'recent_bookings': recent_bookings,
    })





def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seat_class = request.GET.get('seat_class', 'economy')
    passengers = request.GET.get('passengers', '1')
    fare_classes = [
        ('economy', flight.economy_price, '🪑'),
        ('business', flight.business_price, '💼'),
        ('first', flight.first_class_price, '🌟'),
    ]
    return render(request, 'reservations/flight_detail.html', {
        'flight': flight, 'seat_class': seat_class,
        'passengers': passengers, 'fare_classes': fare_classes,
    })
