import json

from django.template.defaultfilters import title
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='Books')

    def test_get_all_category(self):
        url = reverse('category-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data[0]['title'], title(self.category.title))

    def test_create_category(self):
        data = json.dumps({
            'title': "technology",  # Passa uma lista de IDs
        })

        url = reverse('category-list', kwargs={'version': 'v1'})
        response = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(title="technology")
        self.assertEqual(created_category.title, "technology")
