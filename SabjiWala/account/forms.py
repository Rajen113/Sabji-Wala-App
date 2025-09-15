import base64
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'phone', 'age', 'password1', 'password2')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'customer'
        if commit:
            user.save()
        return user


class SellerRegistrationForm(UserCreationForm):
    government_id = forms.FileField(required=True)
    profile_photo = forms.ImageField(required=True)
    # Hidden input from JS camera capture (Base64 string ayega)
    live_selfie = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CustomUser
        fields = (
            'full_name',
            'email',
            'phone',
            'government_id',
            'profile_photo',
            'live_selfie',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'seller'
        user.is_verified = False  # seller needs verification

        # Handle live selfie (Base64 → Image file)
        live_selfie_data = self.cleaned_data.get("live_selfie")
        if live_selfie_data:
            format, imgstr = live_selfie_data.split(';base64,')
            ext = format.split('/')[-1]  # e.g. png / jpg
            user.live_selfie.save(
                f"selfie.{ext}",
                ContentFile(base64.b64decode(imgstr)),
                save=False
            )

        if commit:
            user.save()
        return user



class CustomerLogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
