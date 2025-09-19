from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---- Signup Routes ----
    path('signup/', views.signup_choice, name='signup_choice'),  # 👈 new choice page
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/seller/', views.register_seller, name='register_seller'),
]


