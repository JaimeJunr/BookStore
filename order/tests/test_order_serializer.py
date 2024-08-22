from django.test import TestCase

from order.serializer import OrderSerializer
from order.factories import OrderFactory
from product.factories import ProductFactory


class TestOrderSerializer(TestCase):
    def setUp(self):
        self.product1 = ProductFactory()
        self.product2 = ProductFactory()

        self.order = OrderFactory(product=(self.product1, self.product2))
        self.order_serializer = OrderSerializer(self.order)

    def test_order_serializer_valid(self):
        serializer_data = self.order_serializer.data
        self.assertEquals(
            serializer_data["product"][0]["title"], self.product1.title)
        self.assertEquals(
            serializer_data["product"][1]["title"], self.product2.title)

