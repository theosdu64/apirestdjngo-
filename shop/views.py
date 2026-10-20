from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer


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


class CategoryViewSet(ActiveFilterMixin, ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ActiveFilterMixin, ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_param = 'category_id'
    filter_field = 'category_id'


class ArticleViewSet(ActiveFilterMixin, ReadOnlyModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_param = 'product_id'
    filter_field = 'product_id'
