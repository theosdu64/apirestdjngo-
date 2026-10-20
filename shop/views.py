from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
