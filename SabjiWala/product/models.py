from django.db import models
from django.conf import settings

class Sabji(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sabjis'
    )
    sabji_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    product_img = models.ImageField(upload_to="sabji_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sabji_name} - {self.user.full_name} - ₹{self.price}"

    @property
    def formatted_price(self):
        return f"₹{self.price:.2f}"

    @property
    def seller_name(self):
        return self.user.full_name
