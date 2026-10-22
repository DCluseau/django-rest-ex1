from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'price', 'product']

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError('Price must be greater than 1')
        return value

    def validate_product(self, value):
        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value


# Endpoint pour la liste des products
class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category']

class ProductDetailSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']

    # Validation du nom de la Category
    def validate_name(self, value):
        # Vérification que la Category n'existe pas
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists.')
        return value

    # Validation que le nom de la Category est également dans le champ description
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description.')
        return data

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # Serializer = objet qui permet de transformer les models Django en un autre format
    # Ici, le format est JSON
    class Meta:
        model = Category
        # Champs du model à transformer
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data

