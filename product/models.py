from django.db import models
from user.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    image = models.ImageField()
    description = models.TextField(null=True)


    def __str__(self):
        return (
            f"id: {self.id} | "
            f"product_name: {self.product_name} | "
            f"price: {self.price} | "
            f"description: {self.description if self.description is not None else 'Trống'} | "
            f"user_id: {self.user.id}"
        )