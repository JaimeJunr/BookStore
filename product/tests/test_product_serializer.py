from django.test import TestCase

from product.factories import ProductFactory
from product.serializer import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.product_serializer = ProductSerializer(self.product)

    def test_product_serializer_valid(self):
        serializer_data = self.product_serializer.data
        print(serializer_data)
        self.assertEqual(serializer_data["title"], self.product.title)
