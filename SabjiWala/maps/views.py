from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from account.models import CustomUser
from .models import SabjiRequest
import json
from math import radians, cos, sin, asin, sqrt

# Haversine distance in meters
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    r = 6371000
    return c * r

@login_required
@csrf_exempt
def update_location(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        if latitude and longitude:
            user = request.user
            user.latitude = float(latitude)
            user.longitude = float(longitude)
            user.save()
            return JsonResponse({"status":"success","message":"Location updated"})
        return JsonResponse({"status":"error","message":"Invalid data"}, status=400)
    return JsonResponse({"status":"error","message":"Invalid request"}, status=400)

@login_required
@csrf_exempt
def request_sabji(request):
    if request.method == "POST":
        veg = request.POST.get("vegetable","Sabji Needed")
        SabjiRequest.objects.create(customer=request.user, vegetable=veg)
        return JsonResponse({"status":"success","message":"Sabji request sent"})
    return JsonResponse({"status":"error","message":"Invalid request"}, status=400)

# Customer: nearby sellers
@login_required
def all_sellers(request):
    user = request.user
    if not user.latitude or not user.longitude:
        return JsonResponse([], safe=False)
    # Get all sellers with latitude and longitude
    sellers = CustomUser.objects.filter(user_type="seller")
    print(sellers)
    nearby_sellers = []
    for s in sellers:
        distance = haversine(user.latitude, user.longitude, s.latitude, s.longitude)
        if distance <= 100000000:  # 1 km
            nearby_sellers.append({
                "id": s.id,
                "name": s.full_name,
                "phone": s.phone,
                "photo": s.profile_photo.url if s.profile_photo else "",
                "lat": s.latitude,
                "lng": s.longitude
            })
    print(nearby_sellers)
    return JsonResponse(nearby_sellers, safe=False)


# Customer map page
@login_required
def nearby_sellers_map(request):
    user = request.user

    if user.user_type == "customer":
        # Get all sellers with coordinates
        sellers = CustomUser.objects.filter(user_type="seller").exclude(latitude__isnull=True).exclude(longitude__isnull=True)

        seller_list = []
        for s in sellers:
            seller_list.append({
                "id": s.id,
                "name": s.full_name,
                "phone": s.phone,
                "photo": s.profile_photo.url if s.profile_photo else "",
                "lat": s.latitude,
                "lng": s.longitude
            })
        print(seller_list)
        context = {"sellers": seller_list}
        return render(request, "maps/nearby_sellers_map.html", context)

    # Seller dashboard map
    return render(request, "maps/seller_dashboard_map.html")

@login_required
def nearby_customers(request):
    requests = SabjiRequest.objects.select_related('customer').all()
    customers_dict = {}
    for r in requests:
        c = r.customer
        if c.latitude and c.longitude:
            if c.id not in customers_dict:
                customers_dict[c.id] = {
                    "id": c.id,
                    "name": c.full_name,
                    "lat": c.latitude,
                    "lng": c.longitude,
                    "requests": [r.vegetable] if r.vegetable else []
                }
            else:
                if r.vegetable:
                    customers_dict[c.id]["requests"].append(r.vegetable)
    nearby = list(customers_dict.values())
    return JsonResponse(nearby, safe=False)


# Seller map page
@login_required
def seller_dashboard_map(request):
    if request.user.user_type == "seller":
        return render(request, "maps/seller_dashboard_map.html")
    return render(request, "maps/nearby_sellers_map.html")
