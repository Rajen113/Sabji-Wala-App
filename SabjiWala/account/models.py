from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db.models import Q, UniqueConstraint
from django.db.models.functions import Lower

USER_TYPES = (
    ('admin', 'Admin'),
    ('customer', 'Customer'),
    ('seller', 'Seller'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email) 
        user = self.model(email=email, full_name=full_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(email, full_name, phone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    # Customer-specific
    age = models.PositiveIntegerField(null=True, blank=True)

    # Seller
    government_id = models.FileField(upload_to='documents/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='seller_photos/', null=True, blank=True)
    live_selfie = models.ImageField(upload_to='seller_selfies/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)



    email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('email'),
                name='unique_lower_email'
            )
        ]

    def __str__(self):
        return f"{self.full_name} ({self.user_type})"
