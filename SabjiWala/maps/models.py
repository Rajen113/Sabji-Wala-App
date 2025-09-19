from django.db import models
from account.models import CustomUser

class LocationLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SabjiRequest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requests_made")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="requests_received")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")  # pending / accepted / rejected

    def __str__(self):
        return f"{self.customer.full_name} -> {self.seller.full_name}"
