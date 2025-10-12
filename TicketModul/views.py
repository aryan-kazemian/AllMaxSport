from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer
import traceback


class IsAuthenticatedAndOwnerOrStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if isinstance(obj, Ticket):
            return obj.customer == request.user

        if isinstance(obj, Message):
            return obj.ticket.customer == request.user

        return False


class TicketAPIView(APIView):
    
    permission_classes = [IsAuthenticatedAndOwnerOrStaff]

    def get_queryset(self, request):
        if request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(customer=request.user)

    def get(self, request, *args, **kwargs):
        filters = {}
        for field in ['id', 'status', 'priority', 'related_order_id']:
            val = request.query_params.get(field)
            if val:
                filters[field if field != 'id' else 'pk'] = val

        tickets = self.get_queryset(request).filter(**filters)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            ticket_id = request.query_params.get('id')

            if ticket_id:
                ticket = get_object_or_404(Ticket, pk=ticket_id)

                if not request.user.is_staff and ticket.customer != request.user:
                    return Response({"error": "You cannot add messages to someone else's ticket."},
                                    status=status.HTTP_403_FORBIDDEN)

                serializer = MessageSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(ticket=ticket)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = request.data.copy()
            data['customer'] = request.user.id
            data['customer_name'] = request.user.get_full_name() or request.user.username
            data['created_at'] = timezone.now()
            data['updated_at'] = timezone.now()

            serializer = TicketSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('id')
        message_id = request.query_params.get('message_id')

        if ticket_id:
            ticket = get_object_or_404(Ticket, pk=ticket_id)

            if not request.user.is_staff:
                return Response({'error': 'Only staff can update tickets.'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated_at=timezone.now())
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if message_id:
            message = get_object_or_404(Message, pk=message_id)
            if not request.user.is_staff and message.ticket.customer != request.user:
                return Response({'error': 'You cannot edit messages not in your tickets.'},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = MessageSerializer(message, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Missing id or message_id"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('id')
        message_id = request.query_params.get('message_id')

        if not request.user.is_staff:
            return Response({'error': 'Only staff can delete tickets or messages.'},
                            status=status.HTTP_403_FORBIDDEN)

        if ticket_id:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            ticket.delete()
            return Response({"message": "Ticket deleted"}, status=status.HTTP_200_OK)

        if message_id:
            message = get_object_or_404(Message, pk=message_id)
            message.delete()
            return Response({"message": "Message deleted"}, status=status.HTTP_200_OK)

        return Response({"error": "Missing id or message_id"}, status=status.HTTP_400_BAD_REQUEST)
