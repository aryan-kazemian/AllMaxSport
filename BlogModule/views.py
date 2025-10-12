from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog, Tag, Category
from .serializers import BlogSerializer, TagSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from UserModule.permissions import IsStaffUser

class BlogAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStaffUser()]

    def get(self, request):
        if request.GET.get('tags') == 'true':
            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)

        filters = {}
        if 'id' in request.GET:
            filters['id'] = request.GET.get('id')
        if 'title' in request.GET:
            filters['title__icontains'] = request.GET.get('title')
        if 'status' in request.GET:
            filters['status'] = request.GET.get('status')
        if 'seo_score' in request.GET:
            filters['seo_score'] = request.GET.get('seo_score')
        if 'seo_score_color' in request.GET:
            filters['seo_score_color'] = request.GET.get('seo_score_color')

        blogs = Blog.objects.filter(**filters).prefetch_related('tags').select_related('seo_status', 'category')

        if 'tags' in request.GET and request.GET.get('tags') != 'true':
            blogs = blogs.filter(tags__name__icontains=request.GET.get('tags'))

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.GET.get('tag') == 'true':
            tag_name = request.data.get('tag_name')
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                return Response({'id': tag.id, 'name': tag.name, 'created': created})
            return Response({'error': 'tag_name required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save()
            return Response({'message': 'Blog created', 'id': blog.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        blog_id = request.GET.get('id')
        if not blog_id:
            return Response({'error': 'Blog id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Blog and SEOStatus updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        blog_id = request.GET.get('id')
        category_id = request.GET.get('category_id')

        if blog_id:
            try:
                blog = Blog.objects.get(id=blog_id)
                blog.delete()
                return Response({'message': 'Blog deleted successfully'})
            except Blog.DoesNotExist:
                return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        elif category_id:
            try:
                category = Category.objects.get(id=category_id)
                category.delete()
                return Response({'message': 'Category deleted successfully'})
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'No id or category_id provided'}, status=status.HTTP_400_BAD_REQUEST)
