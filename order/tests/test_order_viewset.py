import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory
from product.models import Product, Category



class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        # Criação do usuário e produtos aqui
        self.user = UserFactory()
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(title='Mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product], user=self.user)

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        Order.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()


    def test_order(self):
        url = reverse('order-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = response.json()
        print('--------------------------------------------------------')
        print(f'DATA: {order_data}')

        self.assertGreater(len(order_data['results']), 0)
        self.assertGreater(len(order_data['results'][0]['product']), 0)

        self.assertEqual(order_data['results'][0]['product'][0]['title'], self.product.title.title())
        self.assertEqual(order_data['results'][0]['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['results'][0]['product'][0]['active'], self.product.active)
        self.assertEqual(order_data['results'][0]['product'][0]['category'][0]['title'], self.category.title)

    def test_create_order(self):
        product = ProductFactory()  # Create a new product
        data = json.dumps({"products_id": [product.id], "user": self.user.id})

        print(data)
        url = reverse('order-list', kwargs={'version': 'v1'})
        response = self.client.post(
            url,
            data=data,
            content_type="application/json",
        )

        print(f'ISSO AI: {response.content}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.filter(user=self.user).last()
        self.assertIsNotNone(created_order)
