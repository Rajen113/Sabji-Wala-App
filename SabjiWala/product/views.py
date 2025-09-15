from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SabjiForm
from .models import Sabji

def add_sabji(request):
    # Only allow sellers
    
    if not request.user.is_authenticated or request.user.user_type != 'seller':
        messages.error(request, "Only sellers can add Sabji items.")
        return redirect('home')

    if request.method == 'POST':
        form = SabjiForm(request.POST)
        if form.is_valid():
            sabji = form.save(commit=False)
            sabji.user = request.user
            sabji.save()
            messages.success(request, "Sabji added successfully!")
            return redirect('home')
    else:
        form = SabjiForm()

    return render(request, 'product/add_sabji.html', {'form': form})
