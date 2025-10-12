from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer
from django.contrib.auth import get_user_model

class ProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        User = get_user_model()
        self.staff_user = User.objects.create_user(
            username="admin",
            password="admin123",
            is_staff=True
        )
        self.client.force_authenticate(user=self.staff_user)

        self.category = Category.objects.create(name="Fitness")
        self.product = Product.objects.create(
            name="Treadmill",
            price=500.0,
            sale_price=450.0,
            stock=10,
            category=self.category,
            product_type="Cardio",
            brand="FitBrand",
            material="Steel",
            weight_capacity=150,
            display="LCD",
            motor_power="2HP",
            product_weight=60.0,
            weight=60.0,
            dimensions="200x80x120",
            description="High quality treadmill",
            warranty="2 years",
            status="active",
            sales=0,
            features=["foldable", "heart rate monitor"],
            images=["image1.jpg", "image2.jpg"]
        )

        self.product_data = {
            "name": "Elliptical",
            "price": 700.0,
            "sale_price": 650.0,
            "stock": 5,
            "category": "Fitness",
            "product_type": "Cardio",
            "brand": "FitBrand",
            "material": "Steel",
            "weight_capacity": 120,
            "product_weight": 50.0,
            "weight": 50.0,
            "dimensions": "180x70x120",
            "description": "Elliptical machine",
            "warranty": "2 years",
            "status": "active",
            "features": ["LCD display"],
            "images": ["image3.jpg"]
        }

    def test_create_product_serializer(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.name, self.product_data['name'])
        self.assertEqual(product.category.name, "Fitness")
        self.assertEqual(product.price, 700.0)
        self.assertEqual(product.product_weight, 50.0)

    def test_update_product_serializer(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        update_data = {"price": 750.0}
        serializer = ProductSerializer(product, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_product = serializer.save()
        self.assertEqual(updated_product.price, 750.0)

    def test_get_products_list(self):
        response = self.client.get(reverse("product-category-api"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product.name)

    def test_filter_products_by_name(self):
        response = self.client.get(reverse("product-category-api") + "?name=Treadmill")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Treadmill")

    def test_create_product(self):
        response = self.client.post(reverse("product-category-api"), self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(name="Elliptical").price, 700.0)

    def test_update_product(self):
        update_data = {"price": 550.0}
        response = self.client.patch(
            reverse("product-category-api") + f"?id={self.product.id}", update_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), 550.0)

    def test_delete_product(self):
        response = self.client.delete(reverse("product-category-api") + f"?id={self.product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_show_categories(self):
        response = self.client.get(reverse("product-category-api") + "?show_categories=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Fitness")
