from django.db import models
from django.contrib.auth.models import User

from product.models.product import Product



# Create your models here.
class Order(models.Model):
    product = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
