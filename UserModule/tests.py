from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "user@example.com",
            "password": "Testpass123!",
            "password2": "Testpass123!",
            "phone": "01234567890"
        }
        self.user = User.objects.create_user(
            username="existinguser",
            email="exist@example.com",
            password="ExistingPass123!",
            phone="09876543210"
        )

        self.register_url = "/api/user/register/"
        self.login_url = "/api/user/login/"
        self.logout_url = "/api/user/logout/"
        self.me_url = "/api/user/me/"

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")

    def test_register_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "Mismatch123!"
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            "username": self.user.username,
            "password": "ExistingPass123!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": self.user.username,
            "password": "WrongPass!"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unauthenticated_user(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_current_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_current_user_requires_authentication(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_model_fields(self):
        self.assertEqual(self.user.username, "existinguser")
        self.assertFalse(self.user.profile_image.name)  # ImageField has .name, not None
        self.assertEqual(self.user.phone, "09876543210")
        self.assertEqual(self.user.user_type, "user")
