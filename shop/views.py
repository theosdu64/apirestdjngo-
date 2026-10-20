from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ArticleSerializer, ArticleAdminSerializer, CategoryAdminSerializer,
)


class ActiveFilterMixin:

    filter_param = None
    filter_field = None

    def get_queryset(self):
        queryset = super().get_queryset().filter(active=True)
        if self.filter_param:
            value = self.request.query_params.get(self.filter_param)
            if value is not None:
                queryset = queryset.filter(**{self.filter_field: value})
        return queryset


class DetailSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class:
            return self.detail_serializer_class
        return super().get_serializer_class()


class CategoryViewSet(ActiveFilterMixin, DetailSerializerMixin, ReadOnlyModelViewSet):

    queryset = Category.objects.order_by('id')
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ProductViewSet(ActiveFilterMixin, DetailSerializerMixin, ReadOnlyModelViewSet):

    queryset = Product.objects.order_by('id')
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    filter_param = 'category_id'
    filter_field = 'category_id'

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ArticleViewSet(ActiveFilterMixin, ReadOnlyModelViewSet):

    queryset = Article.objects.order_by('id')
    serializer_class = ArticleSerializer
    filter_param = 'product_id'
    filter_field = 'product_id'


class AdminCategoryViewSet(ModelViewSet):

    queryset = Category.objects.order_by('id')
    serializer_class = CategoryAdminSerializer


class AdminArticleViewSet(ModelViewSet):

    queryset = Article.objects.order_by('id')
    serializer_class = ArticleAdminSerializer
