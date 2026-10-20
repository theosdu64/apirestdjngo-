from rest_framework.serializers import ModelSerializer, SerializerMethodField

from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'price', 'product']


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class ProductDetailSerializer(ModelSerializer):

    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'articles']

    def get_articles(self, instance):
        active_articles = instance.articles.filter(active=True)
        return ArticleSerializer(active_articles, many=True).data


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryDetailSerializer(ModelSerializer):

    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

    def get_products(self, instance):
        active_products = instance.products.filter(active=True)
        return ProductDetailSerializer(active_products, many=True).data
