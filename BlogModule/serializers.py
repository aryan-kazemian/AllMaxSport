from rest_framework import serializers
from .models import Blog, Tag, SEOStatus, Category

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = Tag
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = Category
        fields = ['id', 'name']


class SEOStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOStatus
        fields = [
            'title_length_status', 'title_length_message',
            'content_length_status', 'content_length_message',
            'keyword_density_status', 'keyword_density_message',
            'meta_description_status', 'meta_description_message',
            'headings_status', 'headings_message',
            'images_status', 'images_message',
            'internal_links_status', 'internal_links_message'
        ]


class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    seo_status = SEOStatusSerializer(required=False)
    category = CategorySerializer(required=False)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'author', 'content', 'excerpt',
            'meta_description', 'keywords', 'status', 'tags',
            'featured_image', 'modify_date', 'seo_score',
            'seo_score_color', 'seo_status', 'category'
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        seo_data = validated_data.pop('seo_status', None)
        category_data = validated_data.pop('category', None)

        if category_data:
            category, _ = Category.objects.get_or_create(name=category_data.get('name'))
            validated_data['category'] = category

        blog = Blog.objects.create(**validated_data)

        for tag_item in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_item['name'])
            blog.tags.add(tag)

        if seo_data:
            SEOStatus.objects.create(blog=blog, **seo_data)

        return blog

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        seo_data = validated_data.pop('seo_status', None)
        category_data = validated_data.pop('category', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if category_data:
            category, _ = Category.objects.get_or_create(name=category_data.get('name'))
            instance.category = category

        instance.save()

        if tags_data:
            instance.tags.clear()
            for tag_item in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_item['name'])
                instance.tags.add(tag)

        if seo_data and hasattr(instance, 'seo_status'):
            seo = instance.seo_status
            for attr, value in seo_data.items():
                setattr(seo, attr, value)
            seo.save()
        elif seo_data:
            SEOStatus.objects.create(blog=instance, **seo_data)

        return instance
