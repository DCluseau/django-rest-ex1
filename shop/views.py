from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from shop.models import Category, Article
from shop.serializers import CategorySerializer, ArticleSerializer

from shop.models import Product

# Utiliser ReadOnlyViewSet pour empêcher de modifier les catégories
class CategoryViewSet(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    # Modification de query_set pour filtrer uniquement les Product actifs
    def get_queryset(self):
        return Category.objects.filter(active=True)

class ProductViewSet(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        # Appliquer un filtre pour n'avoir que les Product actifs
        queryset = Product.objects.filter(active=True)

        # Récupérer la category_id appelée dans l'URL (avec GET.get()
        category_id = self.request.GET.get('category_id')
        # Vérifier si category_id existe
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        # Note : si la category_id n'est pas trouvée, l'application renvoie une liste vide au lieu d'une erreur
        return queryset

class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

