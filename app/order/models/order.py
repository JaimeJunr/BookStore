from django.contrib.auth.models import User
from django.db import models

from product.models.product import Product


class Order(models.Model):
    product = models.ManyToManyField(Product, blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
