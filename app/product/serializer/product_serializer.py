from rest_framework import serializers
from product.models import Category, Product
from product.serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    # 'category' para leitura, exibe detalhes das categorias associadas
    category = CategorySerializer(read_only=True, many=True)
    # 'categories_id' para escrita, utiliza chaves primárias das categorias
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "categories_id",
        ]

    def create(self, validated_data):
        # Remove 'categories_id' dos dados validados
        category_data = validated_data.pop("categories_id", [])
        # Cria o objeto Product com os dados restantes
        product = Product.objects.create(**validated_data)

        # Se houver dados de categorias, associá-las ao produto
        if category_data:
            product.category.set(category_data)
        else:
            raise serializers.ValidationError(
                "At least one category must be provided.")

        return product
