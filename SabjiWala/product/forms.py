from django import forms
from .models import Sabji

class SabjiForm(forms.ModelForm):
    class Meta:
        model = Sabji
        fields = ['sabji_name', 'price', 'quantity', 'product_img']
        widgets = {
            'sabji_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sabji Name'}),
            'price': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Price'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Quantity'}),
        }
