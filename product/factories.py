import factory

from product.models import Category, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    """Fábrica para criar instâncias de Category com dados simulados."""
    title = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("sentence")
    active = factory.Iterator([True, False])

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    """Fábrica para criar instâncias de Product com dados simulados."""
    title = factory.Faker("word")
    price = factory.Faker("random_int", min=100, max=1000)
    category = factory.RelatedFactory(CategoryFactory, factory_related_name='product')

    class Meta:
        model = Product

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        """Adiciona categorias ao produto após sua criação.

              Se 'extracted' for passado, as categorias especificadas são adicionadas.
              Caso contrário, uma categoria padrão é criada e associada ao produto.
              """
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)
        else:
            self.category.add(CategoryFactory())
