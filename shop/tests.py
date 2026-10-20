from django.urls import reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product


class ShopTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fruits = Category.objects.create(name='Fruits', active=True)
        cls.legumes = Category.objects.create(name='Légumes', active=True)
        Category.objects.create(name='Caché', active=False)

        cls.ananas = Product.objects.create(name='Ananas', category=cls.fruits, active=True)
        cls.tomate = Product.objects.create(name='Tomate', category=cls.legumes, active=True)
        Product.objects.create(name='Banane', category=cls.fruits, active=False)

    def get_ids(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return [item['id'] for item in response.json()['results']]


class CategoryTests(ShopTestCase):

    def test_list_returns_only_active_categories(self):
        ids = self.get_ids(reverse('category-list'))
        self.assertEqual(ids, [self.fruits.id, self.legumes.id])

    def test_post_is_not_allowed(self):
        response = self.client.post(reverse('category-list'), {'name': 'Nouvelle'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Category.objects.count(), 3)


class ProductTests(ShopTestCase):

    def test_list_returns_only_active_products(self):
        ids = self.get_ids(reverse('product-list'))
        self.assertEqual(ids, [self.ananas.id, self.tomate.id])

    def test_filter_by_category(self):
        ids = self.get_ids(reverse('product-list') + f'?category_id={self.legumes.id}')
        self.assertEqual(ids, [self.tomate.id])
