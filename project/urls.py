from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# from shop.views import CategoryView
from shop.views import CategoryViewSet
# from shop.views import ProductView
from shop.views import ProductViewSet

# Création du router
router = routers.SimpleRouter()

# Création de l'adresse générique pour Category api/category
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # Il faut ajouter la ligne suivante pour prendre en compte le router
    path('api/', include(router.urls)),
    # path('api/category/', CategoryView.as_view()),
    # path('api/product/', ProductView.as_view())
]
