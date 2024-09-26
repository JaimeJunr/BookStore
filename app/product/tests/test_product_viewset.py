import json

from django.template.defaultfilters import title
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    """
    Suite de testes para o ProductViewSet, que lida com a API de produtos.

    Esta classe utiliza a infraestrutura do Django REST Framework para testar
    as funcionalidades de criação, listagem e manipulação de produtos na API.
    """

    client = APIClient()

    def setUp(self):
        """
        Configura o ambiente de teste antes de cada método de teste ser executado.

        Cria um usuário autenticado, uma categoria padrão e um produto padrão para uso nos testes.
        """
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()
        self.client.force_authenticate(user=self.user)
        self.default_category = CategoryFactory()
        self.product = ProductFactory(title="Pro Controller", price=200)

    def get_product_list_url(self):
        """
        Retorna a URL para a lista de produtos da API.

        Returns:
            str: URL da rota `product-list` com a versão da API.
        """
        return reverse("product-list", kwargs={"version": "v1"})

    def create_product_payload(self, title="notebook", price=900.00, categories=None):
        """
        Cria um payload de dados JSON para criar um novo produto.

        Args:
            title (str): Título do produto. Default: "notebook".
            price (float): Preço do produto. Default: 900.00.
            categories (list): Lista de IDs de categorias associadas ao produto. Default: None.

        Returns:
            dict: Dicionário contendo os dados do produto para a criação via API.
        """
        if categories is None:
            categories = [self.default_category.id]
        return {
            "title": title,
            "price": price,
            "categories_id": categories,
        }

    def test_get_all_products(self):
        """
        Testa o endpoint de listagem de todos os produtos.

        Este teste faz uma requisição GET à rota de listagem de produtos e verifica se o
        status da resposta é 200 OK. Também compara os dados retornados com o produto criado
        no `setUp`.
        """
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        url = self.get_product_list_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = json.loads(response.content)

        self.assertEqual(
            product_data["results"][0]["title"], self.product.title.title()
        )
        self.assertEqual(product_data["results"]
                         [0]["price"], self.product.price)
        self.assertEqual(product_data["results"]
                         [0]["active"], self.product.active)

    def test_create_product(self):
        """
        Testa o endpoint de criação de um novo produto.

        Este teste faz uma requisição POST à rota de criação de produtos utilizando um payload
        de dados gerado pelo método `create_product_payload`. Verifica se o status da resposta
        é 201 CREATED e se o produto foi criado corretamente no banco de dados.
        """
        url = self.get_product_list_url()
        data = self.create_product_payload()

        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title=data["title"])

        self.assertEqual(created_product.title, data["title"])
        self.assertEqual(created_product.price, data["price"])
