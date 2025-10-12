from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    stock = serializers.IntegerField(required=False, allow_null=True, default=0)
    product_type = serializers.CharField(required=False, allow_blank=True, default='')
    material = serializers.CharField(required=False, allow_blank=True, default='')
    product_weight = serializers.FloatField(required=False, allow_null=True, default=0.0)
    weight = serializers.FloatField(required=False, allow_null=True, default=0.0)
    dimensions = serializers.CharField(required=False, allow_blank=True, default='')
    warranty = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = Product
        fields = '__all__'

    def to_internal_value(self, data):
        if 'category' in data and isinstance(data['category'], dict):
            data['category'] = data['category'].get('name', None)
        return super().to_internal_value(data)

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)
        if category_name:
            category_obj, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category_obj
        return super().create(validated_data)

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        if category_name:
            category_obj, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category_obj
        return super().update(instance, validated_data)
