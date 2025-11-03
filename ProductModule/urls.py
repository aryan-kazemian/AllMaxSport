from django.urls import path
from .views import ProductCategoryAPIView, CategoryAPIView

urlpatterns = [
    path('', ProductCategoryAPIView.as_view(), name='product-category-api'),
    path('categories/', CategoryAPIView.as_view(), name='category-api'),
]
