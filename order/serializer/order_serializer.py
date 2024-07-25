from rest_framework import serializers

from product.models import Product
from product.serializer.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(require=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        model = Product
        fields = ['product', 'total']
