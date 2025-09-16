from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomerRegistrationForm, SellerRegistrationForm, CustomerLogInForm,LocationForm
from django.core.mail import send_mail
from django.conf import settings
from geopy.geocoders import Nominatim

def home(request):
    return render(request, 'account/base.html')


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            
            # Send welcome email
            
            subject = 'Welcome to SabjiWala App'
            message = f'Hi {user.full_name},\n\nThank you for registering at SabjiWala App!'
            from_email = settings.EMAIL_HOST_USER or 'noreply@sabjiwala.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, 'Customer registered successfully! Check your email.')
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'account/register_customer.html', {'form': form})


def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seller registered successfully! Please wait for verification.')
            return redirect('login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'account/register_seller.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomerLogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = CustomerLogInForm()
    return render(request, 'account/login.html', {'form': form})


# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('home')


def map_view(request):
    geolocator = Nominatim(user_agent="account")

    form = LocationForm(request.GET or None)
    start_city = None
    end_city = None
    context = {} 

    if form.is_valid():
        start_city = form.cleaned_data['start_location']
        end_city = form.cleaned_data['end_location']
        print("Start:", start_city, " End:", end_city)

        start_location = geolocator.geocode(start_city)
        end_location = geolocator.geocode(end_city)

        if start_location and end_location:
            context = {
                "start": {"lat": start_location.latitude, "lng": start_location.longitude, "name": start_city},
                "end": {"lat": end_location.latitude, "lng": end_location.longitude, "name": end_city},
            }

    return render(request, 'account/map.html', {
        'form': form,
        'context': context,
        'start_city': start_city,
        'end_city': end_city
    })