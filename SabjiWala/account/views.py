from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import CustomerRegistrationForm, SellerRegistrationForm, LoginForm,UserProfileForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def home(request):
    return render(request, "account/home.html")

def about(request):
    return render(request, 'account/about.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission (optional)
        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')
    return render(request, 'account/contact.html')


def signup_choice(request):
    return render(request, "account/signup_choice.html")


def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

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
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)

                if user.user_type == 'customer':
                    return redirect('customer_dashboard')   # clean redirect

                elif user.user_type == 'seller':
                    return redirect('seller_dashboard')     # clean redirect

                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')

def customer_dashboard(request):
    return render(request, 'account/customer_dashboard.html')

def seller_dashboard(request):
    return render(request, 'account/seller_dashboard.html')


@login_required
def user_profile(request):
    user = request.user
    return render(request, "account/profile.html", {"user": user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'account/edit_profile.html', {'form': form})
