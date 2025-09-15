from django.contrib import admin
from .models import Sabji

# Register your models here.

@admin.register(Sabji)
class SabjiAdmin(admin.ModelAdmin):
    list_display=('sabji_name','price','quantity','created_at')
