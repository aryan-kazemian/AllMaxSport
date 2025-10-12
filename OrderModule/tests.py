from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from UserModule.models import User
from ProductModule.models import Product, Category
from .models import Order, OrderItem, DiscountCode


class OrderAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.staff = User.objects.create_user(username="staffuser", password="pass123", is_staff=True)
        self.user = User.objects.create_user(username="regularuser", password="pass123")

        self.category = Category.objects.create(name="TestCategory")

        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            stock=10,
            category=self.category,
            product_type="Test",
            brand="Brand",
            material="Material",
            weight_capacity=100,
            product_weight=50,
            weight=50,
            dimensions="10x10x10",
            description="Test product",
            warranty="1 year",
            status="active",
            sales=0,
            features=[],
            images=[]
        )

        self.discount = DiscountCode.objects.create(code="DISCOUNT20", percentage=20)

        self.api_path = "/api/orders/"

    def test_create_order_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "order_id": "ORD789",
            "order_date": timezone.now(),
            "order_status": "pending_payment",
            "carrier": "UPS",
            "cost": 100,
            "estimated_delivery_date": timezone.now() + timedelta(days=4),
            "method": "standard",
            "code": 4321,
            "subtotal": 100,
            "shipping": 10,
            "tax": 5,
            "total": 115,
            "items": [{"id": self.product.id, "quantity": 1}]
        }
        response = self.client.post(self.api_path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)

    def test_create_order_unauthenticated_forbidden(self):
        data = {"order_id": "ORD000"}
        response = self.client.post(self.api_path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_discount_code_list_staff_only(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.api_path + "?discount_code=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.api_path + "?discount_code=true")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list_user_vs_staff(self):
        order = Order.objects.create(
            order_id="ORD321",
            order_date=timezone.now(),
            order_status="pending_payment",
            customer=self.user,
            customer_name=self.user.username,
            carrier="UPS",
            cost=100,
            estimated_delivery_date=timezone.now() + timedelta(days=5),
            method="standard",
            code=1111,
            subtotal=100,
            shipping=10,
            tax=5,
            total=115
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.api_path)
        self.assertEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.api_path)
        self.assertGreaterEqual(len(response.data), 1)

    def test_delete_order_permission(self):
        order = Order.objects.create(
            order_id="ORD999",
            order_date=timezone.now(),
            order_status="pending_payment",
            customer=self.user,
            customer_name=self.user.username,
            carrier="UPS",
            cost=100,
            estimated_delivery_date=timezone.now() + timedelta(days=5),
            method="standard",
            code=2222,
            subtotal=100,
            shipping=10,
            tax=5,
            total=115
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.api_path + f"?id={order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
