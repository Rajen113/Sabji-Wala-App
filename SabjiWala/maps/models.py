from django.db import models
from account.models import CustomUser

class LocationLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SabjiRequest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vegetable = models.CharField(max_length=100)   # jaise: Aalu, Tamatar
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vegetable} requested by {self.customer.full_name}"
