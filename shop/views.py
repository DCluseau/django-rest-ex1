from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Category
from shop.serializers import CategorySerializer

from shop.models import Product
from shop.serializers import ProductSerializer


class CategoryView(APIView):

    def get(self, *args, **kwargs):
        # Récupérer toutes les catégories (ORM Django)
        queryset = Category.objects.all()
        # Sérialiser les données
        # Si il n'y a qu'un objet à renvoyer, le paramètre "many" peut être ignoré
        serializer = CategorySerializer(queryset, many=True)
        # Renvoyer les réponses au format JSON
        return Response(serializer.data)

class ProductView(APIView):
    def get(self, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)