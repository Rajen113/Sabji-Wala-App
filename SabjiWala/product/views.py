from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Sabji
from .forms import SabjiForm
from account.models import CustomUser

# ------------------------------
# Customer Views
# ------------------------------

@login_required
def seller_list(request):
    """Customer: List all verified sellers"""
    if request.user.user_type != 'customer':
        messages.error(request, "Only customers can view sellers.")
        return redirect('home')

    sellers = CustomUser.objects.filter(user_type='seller', is_verified=True)
    print(sellers)
    return render(request, 'product/seller_list.html', {'sellers': sellers})

@login_required
def seller_products_for_customer(request, seller_id):
    """Customer: List products of a particular seller"""
    print('done1')
    print(request.user.user_type)
    if request.user.user_type != 'customer':
        messages.error(request, "Only customers can view this page.")
        return redirect('home')

    seller = get_object_or_404(CustomUser, id=seller_id, user_type='seller', is_verified=True)
    products = Sabji.objects.filter(user=seller)
    print(products)
    return render(request, 'product/seller_products_customer.html', {'products': products, 'seller': seller})

# ------------------------------
# Seller Views
# ------------------------------

@login_required
def add_sabji(request):
    """Seller: Add a new product"""
    if request.user.user_type != 'seller':
        messages.error(request, "Only sellers can add products.")
        return redirect('home')

    if request.method == 'POST':
        form = SabjiForm(request.POST, request.FILES)
        if form.is_valid():
            sabji = form.save(commit=False)
            sabji.user = request.user
            sabji.save()
            messages.success(request, "Product added successfully!")
            return redirect('seller_sabji_list')
    else:
        form = SabjiForm()

    return render(request, 'product/add_sabji.html', {'form': form})

@login_required
def update_sabji(request, pk):
    """Seller: Update existing product"""
    sabji = get_object_or_404(Sabji, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SabjiForm(request.POST, request.FILES, instance=sabji)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('seller_sabji_list')
    else:
        form = SabjiForm(instance=sabji)

    return render(request, 'product/add_sabji.html', {'form': form})

@login_required
def delete_sabji(request, pk):
    """Seller: Delete a product"""
    sabji = get_object_or_404(Sabji, pk=pk, user=request.user)
    sabji.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('seller_sabji_list')

@login_required
def seller_sabji_list(request):
    """Seller: List all their own products"""
    if request.user.user_type != 'seller':
        messages.error(request, "Only sellers can view this page.")
        return redirect('home')

    products = Sabji.objects.filter(user=request.user)
    return render(request, 'product/seller_sabji_list.html', {'products': products})
