from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-customer/', views.register_customer, name='register_customer'),
    path('register-seller/', views.register_seller, name='register_seller'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
