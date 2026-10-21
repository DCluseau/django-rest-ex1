from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'date_created', 'date_updated', 'name', 'product_id']

# Endpoint pour les products
class ProductSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    # Serializer = objet qui permet de transformer les models Django en un autre format
    # Ici, le format est JSON
    class Meta:
        model = Category
        # Champs du model à transformer
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data

