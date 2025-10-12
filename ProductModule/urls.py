from django.urls import path
from .views import ProductCategoryAPIView

urlpatterns = [
    path('', ProductCategoryAPIView.as_view(), name='product-category-api'),
]
