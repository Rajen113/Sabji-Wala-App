from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.nearby_sellers_map, name='nearby_sellers_map'),  # Customer view
    path('update-location/', views.update_location, name='update_location'),
    path('all-sellers/', views.all_sellers, name='all_sellers'),
    path('nearby-customers/', views.nearby_customers, name='nearby_customers'),  # Seller API
    path('seller/dashboard-map/', views.seller_dashboard_map, name='seller_dashboard_map'),  # Seller view
]
