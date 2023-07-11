from django_filters.rest_framework import FilterSet

from ..models import Ticket


class TicketFilter(FilterSet):
    class Meta:
        model = Ticket
        fields = {
            "title": ["icontains"],
            "description": ["icontains"],
            "created_at": ["date", "date__gt", "date__lt"],
            "current_status": ["exact"],
        }
