import requests
from django.db import models, transaction

OPEN_FOOD_FACTS_URL = 'https://world.openfoodfacts.org/api/v2/product/3274080005003.json'
OPEN_FOOD_FACTS_TIMEOUT = 5


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @transaction.atomic
    def disable(self):
        if not self.active:
            return
        self.active = False
        self.save()
        Article.objects.filter(product__category=self).update(active=False)
        self.products.update(active=False)


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    @transaction.atomic
    def disable(self):
        if not self.active:
            return
        self.active = False
        self.save()
        self.articles.update(active=False)

    def call_external_api(self):
        return requests.get(
            OPEN_FOOD_FACTS_URL,
            params={'fields': 'ecoscore_grade'},
            headers={'User-Agent': 'apiRestDjango-exercice'},
            timeout=OPEN_FOOD_FACTS_TIMEOUT,
        )

    @property
    def ecoscore(self):
        try:
            response = self.call_external_api()
        except requests.RequestException:
            return None
        if response.status_code != 200:
            return None
        return response.json().get('product', {}).get('ecoscore_grade')


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
