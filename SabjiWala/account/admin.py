from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'full_name', 'phone', 'latitude', 'longitude',
        'user_type', 'is_staff', 'is_active', 'is_verified'
    )
    list_filter = ('user_type', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'full_name', 'phone')
    ordering = ('email',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'age')}),
        ('Seller Info', {'fields': ('government_id', 'profile_photo', 'live_selfie', 'is_verified')}),
        ('Location Info', {'fields': ('latitude', 'longitude')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'phone', 'user_type',
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
