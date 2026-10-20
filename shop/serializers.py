from rest_framework.serializers import ModelSerializer

from shop.models import Category


class CategorySerializer(ModelSerializer):

    # Serializer = objet qui permet de transformer les models Django en un autre format
    # Ici, le format est JSON
    class Meta:
        model = Category
        fields = ['id', 'name']
