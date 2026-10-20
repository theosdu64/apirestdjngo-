from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from shop.models import Category, Product, Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'price', 'product']


class ArticleAdminSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = ['id', 'name', 'description', 'price', 'product', 'active']

    def validate_price(self, value):
        if value <= 1:
            raise ValidationError('Le prix doit être supérieur à 1 €.')
        return value

    def validate_product(self, value):
        if not value.active:
            raise ValidationError('Le produit associé doit être actif.')
        return value


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


class CategoryAdminSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'active']

    def validate_name(self, value):
        duplicates = Category.objects.filter(name=value)
        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise ValidationError('Une catégorie portant ce nom existe déjà.')
        return value

    def validate(self, data):
        name = data.get('name', getattr(self.instance, 'name', ''))
        description = data.get('description', getattr(self.instance, 'description', ''))
        if name.lower() not in description.lower():
            raise ValidationError('Le nom doit figurer dans la description.')
        return data


class CategoryDetailSerializer(ModelSerializer):

    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

    def get_products(self, instance):
        active_products = instance.products.filter(active=True)
        return ProductDetailSerializer(active_products, many=True).data
