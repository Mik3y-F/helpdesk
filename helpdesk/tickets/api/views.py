from rest_framework.viewsets import ModelViewSet

from ..models import Ticket, TicketStatus
from .serializers import TicketSerializer, TicketStatusSerializer


class TicketViewSet(ModelViewSet):
    """
    API endpoint that allows tickets to be viewed or edited.
    """

    serializer_class = TicketSerializer
    queryset = Ticket.objects.prefetch_related("statuses").all()


class TicketStatusViewSet(ModelViewSet):
    """
    API endpoint that allows ticket statuses to be viewed or edited.
    """

    serializer_class = TicketStatusSerializer

    def get_queryset(self):
        return TicketStatus.objects.filter(ticket=self.kwargs["ticket_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["ticket_pk"] = self.kwargs["ticket_pk"]
        return context
