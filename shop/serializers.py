from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product


class CategorySerializer(ModelSerializer):

    # Serializer = objet qui permet de transformer les models Django en un autre format
    # Ici, le format est JSON
    class Meta:
        model = Category
        # Champs du model à transformer
        fields = ['id', 'name']

# Endpoint pour les products
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category']
