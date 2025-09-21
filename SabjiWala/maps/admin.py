from django.contrib import admin
from .models import SabjiRequest

@admin.register(SabjiRequest)
class SabjiRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vegetable', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__full_name', 'vegetable')
