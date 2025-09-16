from django.urls import path
from .views import add_sabji

urlpatterns = [
    path('', add_sabji,name='add_product')
]