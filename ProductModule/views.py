from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import AllowAny
from UserModule.permissions import IsStaffUser

class ProductCategoryAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsStaffUser()]

    def get(self, request):
        if request.GET.get('show_categories') == 'true':
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        filters = Q()
        params = request.query_params

        if 'id' in params:
            filters &= Q(id=params['id'])
        if 'name' in params:
            filters &= Q(name__icontains=params['name'])
        if 'max_price' in params:
            filters &= Q(price__lte=params['max_price'])
        if 'min_price' in params:
            filters &= Q(price__gte=params['min_price'])
        if 'max_sale_price' in params:
            filters &= Q(sale_price__lte=params['max_sale_price'])
        if 'min_sale_price' in params:
            filters &= Q(sale_price__gte=params['min_sale_price'])
        if 'category' in params:
            filters &= Q(category__name__icontains=params['category'])
        if 'brand' in params:
            filters &= Q(brand__icontains=params['brand'])
        if 'status' in params:
            filters &= Q(status=params['status'])
        if 'sales' in params:
            filters &= Q(sales=params['sales'])

        products = Product.objects.filter(filters)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({'error': 'Product id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        product_id = request.query_params.get('id')
        if not product_id:
            return Response({'error': 'Product id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
