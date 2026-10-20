# Module pour permettre à l'API de trouver les URLs à tester
from django.urls import reverse_lazy
# Classe de tests de base
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopAPITestCase(APITestCase):
    # Formatage de date en chaîne de caractères sous le même format que celui de l'API
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

class TestCategory(ShopAPITestCase):
    # Stockage de l'URL de l'endpoint dans un attribut de classe
    # Permet de l'utiliser plus facilement dans les tests
    url = reverse_lazy('category-list')

    def test_list(self):
        # Création de deux catégories, une active et une inactive
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        # Utilisation de la méthode get() avec le client de la classe de test
        response = self.client.get(self.url)
        # Vérification du code de retour attendu (=200) ainsi que des valeurs retournées
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,
                'name': category.name
            }
        ]
        self.assertEqual(response.json(), excepted)

    def test_create(self):
        # Vérification qu'une Category n'existe pas avant de la créer pour le test
        self.assertFalse(Category.objects.exists())
        # Création d'une nouvelle Category
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Vérification que la réponse est bien 405 (=erreur)
        self.assertEqual(response.status_code, 405)
        # Vérification qu'aucune nouvelle Category n'a été créée
        self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
    url = reverse_lazy('product-list')

    def get_product_detail_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id
            } for product in products
        ]

    def test_list(self):
        # Initier une Category pour pouvoir créer des Product
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)
        Product.objects.create(name='Kiwi', category=category, active=False)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': product.pk,
                'name': product.name
            }
        ]
        self.assertEqual(response.json(), excepted)

    def test_filter(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)

        response = self.client.get(self.url + '?category=1')
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': product.pk,
                'name': product.name
            }
        ]
        self.assertEqual(response.json(), excepted)

    def test_create(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)

        response = self.client.post(self.url, product_data={'name': 'Banana'})
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        category = Category.objects.create(name='Fruits', active=True)
        product = Product.objects.create(name='Banane', category=category, active=True)

        response = self.client.delete(self.url, product_data={'name': 'Banana'})
        self.assertEqual(response.status_code, 405)