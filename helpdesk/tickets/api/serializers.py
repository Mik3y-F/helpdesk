from rest_framework import serializers

from ..models import Ticket, TicketStatus


class TicketStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for the TicketStatus model
    """

    class Meta:
        model = TicketStatus
        fields = [
            "id",
            "ticket",
            "status",
            "created_at",
        ]
        read_only_fields = (
            "ticket_number",
            "created_at",
        )


class TicketStatusSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for the TicketStatus model
    """

    status = serializers.CharField(source="get_status_display", read_only=True)
    code = serializers.CharField(source="status", read_only=True)

    class Meta:
        model = TicketStatus
        fields = [
            "id",
            "status",
            "code",
            "created_at",
        ]
        read_only_fields = (
            "ticket_number",
            "created_at",
        )


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ticket model
    """

    current_status = serializers.SerializerMethodField(
        method_name="get_current_status",
    )

    def get_current_status(self, ticket: Ticket):
        """
        Get the latest ticket status
        """
        try:
            status = ticket.statuses.latest("created_at")
        except TicketStatus.DoesNotExist:
            status = None

        if status is not None:
            return TicketStatusSummarySerializer(status).data
        else:
            return None  # or some suitable default

    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "current_status",
            "description",
            "ticket_type",
            "user",
            "assigned_to",
            "ticket_number",
            "priority",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "ticket_number",
            "created_at",
            "updated_at",
            "current_status",
        )
