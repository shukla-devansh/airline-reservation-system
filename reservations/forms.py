from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Booking, Passenger


class FlightSearchForm(forms.Form):
    TRIP_CHOICES = [('one_way', 'One Way'), ('round_trip', 'Round Trip')]
    trip_type = forms.ChoiceField(choices=TRIP_CHOICES, widget=forms.RadioSelect)
    origin = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'placeholder': 'From (e.g. DEL)'}))
    destination = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'placeholder': 'To (e.g. BOM)'}))
    departure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    passengers = forms.IntegerField(min_value=1, max_value=9, initial=1)
    seat_class = forms.ChoiceField(choices=[('economy','Economy'),('business','Business'),('first','First Class')])


class BookingForm(forms.Form):
    contact_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    contact_phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}))


class PassengerForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    passport_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Passport Number'}))


PassengerFormSet = forms.formset_factory(PassengerForm, extra=0, min_num=1)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
