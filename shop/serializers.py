from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category']
