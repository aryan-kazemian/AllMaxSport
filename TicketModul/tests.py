from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone

from UserModule.models import User
from .models import Ticket, Message


class TicketAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.staff = User.objects.create_user(username="staffuser", password="pass123", is_staff=True)
        self.user = User.objects.create_user(username="regularuser", password="pass123")
        self.other_user = User.objects.create_user(username="otheruser", password="pass123")

        self.ticket = Ticket.objects.create(
            status="open",
            priority="medium",
            subject="Test Ticket",
            customer=self.user,
            customer_name=self.user.username,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        self.message = Message.objects.create(
            ticket=self.ticket,
            sender="customer",
            text="Initial message",
            timestamp=timezone.now(),
            message="Initial message"
        )

        self.api_path = "/api/tickets/"

    def test_create_ticket_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "status": "open",
            "priority": "high",
            "subject": "New Ticket",
            "related_order_id": "ORD123",
        }
        response = self.client.post(self.api_path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["subject"], "New Ticket")
        self.assertEqual(response.data["customer"], self.user.id)

    def test_create_ticket_unauthenticated_forbidden(self):
        data = {"subject": "Unauthorized Ticket"}
        response = self.client.post(self.api_path, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_message_to_ticket_by_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            "sender": "customer",
            "text": "Spam message",
            "message": "Spam message",
            "timestamp": timezone.now()
        }
        response = self.client.post(self.api_path + f"?id={self.ticket.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ticket_list_staff_vs_user(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.api_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.api_path)
        self.assertEqual(len(response.data), 1)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.api_path)
        self.assertEqual(len(response.data), 0)

    def test_ticket_filters(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.api_path + f"?status=open")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["status"], "open")

        response = self.client.get(self.api_path + f"?priority=medium")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["priority"], "medium")

    def test_update_ticket_staff_only(self):
        self.client.force_authenticate(user=self.staff)
        data = {"status": "closed"}
        response = self.client.patch(self.api_path + f"?id={self.ticket.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, "closed")

    def test_update_ticket_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        data = {"status": "closed"}
        response = self.client.patch(self.api_path + f"?id={self.ticket.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_message_owner_or_staff(self):
        self.client.force_authenticate(user=self.user)
        data = {"text": "Updated message"}
        response = self.client.patch(self.api_path + f"?message_id={self.message.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.text, "Updated message")

    def test_update_message_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"text": "Hack message"}
        response = self.client.patch(self.api_path + f"?message_id={self.message.id}", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ticket_staff_only(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(self.api_path + f"?id={self.ticket.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())

    def test_delete_ticket_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.api_path + f"?id={self.ticket.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_message_staff_only(self):
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(self.api_path + f"?message_id={self.message.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())
