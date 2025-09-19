from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from account.models import CustomUser
from django.shortcuts import render
import json
from math import radians, cos, sin, asin, sqrt

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
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        user = request.user
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        return JsonResponse({"status": "success", "message": "Location updated"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def all_sellers(request):
    user = request.user
    if user.latitude is None or user.longitude is None:
        return JsonResponse([], safe=False)
    sellers = CustomUser.objects.filter(user_type="seller", latitude__isnull=False, longitude__isnull=False)
    nearby = []
    for s in sellers:
        distance = haversine(user.latitude, user.longitude, s.latitude, s.longitude)
        if distance <= 1000:
            nearby.append({
                "id": s.id,
                "name": s.full_name,
                "phone": s.phone,
                "photo": s.profile_photo.url if s.profile_photo else "",
                "lat": s.latitude,
                "lng": s.longitude
            })
    return JsonResponse(nearby, safe=False)

@login_required
def nearby_sellers_map(request):
    return render(request, "maps/nearby_sellers_map.html")

@login_required
def nearby_customers(request):
    seller = request.user
    if seller.latitude is None or seller.longitude is None:
        return JsonResponse([], safe=False)
    customers = CustomUser.objects.filter(user_type="customer", latitude__isnull=False, longitude__isnull=False)
    nearby = []
    for c in customers:
        distance = haversine(seller.latitude, seller.longitude, c.latitude, c.longitude)
        if distance <= 1000:
            nearby.append({
                "id": c.id,
                "name": c.full_name,
                "phone": c.phone,
                "lat": c.latitude,
                "lng": c.longitude
            })
    return JsonResponse(nearby, safe=False)

@login_required
def seller_dashboard_map(request):
    return render(request, "maps/seller_dashboard_map.html")
