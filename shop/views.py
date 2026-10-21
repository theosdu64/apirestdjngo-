from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ArticleSerializer, ArticleAdminSerializer, CategoryAdminSerializer,
)


class CategoryViewSet(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True).order_by('id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ProductViewSet(ReadOnlyModelViewSet):

    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True).order_by('id')
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ArticleViewSet(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.filter(active=True).order_by('id')
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class AdminCategoryViewSet(ModelViewSet):

    serializer_class = CategoryAdminSerializer

    def get_queryset(self):
        return Category.objects.order_by('id')


class AdminArticleViewSet(ModelViewSet):

    serializer_class = ArticleAdminSerializer

    def get_queryset(self):
        return Article.objects.order_by('id')
