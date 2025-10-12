from rest_framework import serializers
from .models import Ticket, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'status', 'priority', 'subject', 'related_order_id', 'customer', 'customer_name', 'created_at',
             'updated_at', 'resolved_at', 'messages',
        ]
