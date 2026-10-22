from django.db import transaction
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response

from shop.models import Category, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ArticleSerializer, ProductListSerializer

from shop.models import Product

class MultipleSerializerMixin:
    # Un mixin est une classe qui ne fonctionne pas de façon autonome
    # Elle permet d'ajouter des fonctionnalités aux classes qui les étendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # Notre mixin détermine quel serializer à utiliser
        # même si elle ne sait pas ce que c'est ni comment l'utiliser
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # Si l'action demandée est le détail alors nous retournons le serializer de détail
            return self.detail_serializer_class
        return super().get_serializer_class()


# Utiliser ReadOnlyViewSet pour empêcher de modifier les catégories
class CategoryViewSet(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    # Attribut de classe pour définir un serializer de détails
    detail_serializer_class = CategoryDetailSerializer

    # Modification de query_set pour filtrer uniquement les Product actifs
    def get_queryset(self):
        return Category.objects.filter(active=True)

    def get_serializer_class(self):
        # Si l'action est retrieve, alors retour du serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Désactivation de la Category
        self.get_object().disable()
        category = self.get_object()
        category.active = False
        category.save()

        # Désactivation des produits de la Category
        category.products.update(active=False)

        # Retour du status_code 200 pour indiquer le succès de l'action
        return Response()

class ProductViewSet(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer

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

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Désactivation de la Category
        self.get_object().disable()
        product = self.get_object()
        product.active = False
        product.save()

        # Désactivation des produits de le Product
        product.articles.update(active=False)

        # Retour du status_code 200 pour indiquer le succès de l'action
        return Response()

class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class AdminCategoryViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    # queryset = Category.objects.all()
    def get_queryset(self):
        return Category.objects.all()

class AdminArticleViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        return Article.objects.all()

class AdminProductViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        return Product.objects.all()
