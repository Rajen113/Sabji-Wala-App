
from django.urls import path
from . import views


urlpatterns = [
    # ------------------------------
    # Seller routes (Product Management)
    # ------------------------------
    path('sabji/add/', views.add_sabji, name='add_sabji'),
    path('sabji/update/<int:pk>/', views.update_sabji, name='update_sabji'),
    path('sabji/delete/<int:pk>/', views.delete_sabji, name='delete_sabji'),
    path('sabji/seller/', views.seller_sabji_list, name='seller_sabji_list'),

    # ------------------------------
    # Customer routes
    # ------------------------------
    path('sellers/', views.seller_list, name='seller_list'),  # List all verified sellers
    path('sellers/<int:seller_id>/products/', views.seller_products_for_customer, name='seller_products'),  # List products of a particular seller for customer
]


