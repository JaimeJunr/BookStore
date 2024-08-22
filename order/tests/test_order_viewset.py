import json

from django.template.defaultfilters import title
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from order.factories import OrderFactory
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(title='Mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        url = reverse('order-list', kwargs={'version': 'v1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['product'][0]['title'], title(self.product.title))
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['product'][0]['category'][0]['title'], self.category.title)
