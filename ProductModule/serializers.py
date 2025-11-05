from rest_framework import serializers
from .models import Product, Category


class RecursiveCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    childs = serializers.SerializerMethodField()

    def get_childs(self, obj):
        children = obj.get_children()
        if children.exists():
            return RecursiveCategorySerializer(children, many=True).data
        return []
    



class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    childs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'childs']

    def get_childs(self, obj):
        children = obj.get_children()
        if children.exists():
            return CategorySerializer(children, many=True).data
        return []

    def validate_parent(self, value):
        """Prevent adding a child under another child (max depth = 2)"""
        if value and value.parent is not None:
            raise serializers.ValidationError(
                "Cannot create a child under another child category (max depth = 2)."
            )
        return value




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
