from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Ticket, TicketStatus
from .filters import TicketFilter
from .pagination import DefaultPagination
from .serializers import TicketSerializer, TicketStatusSerializer


class TicketViewSet(ModelViewSet):
    """
    API endpoint that allows tickets to be viewed or edited.
    """

    serializer_class = TicketSerializer
    queryset = Ticket.objects.prefetch_related("statuses").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TicketFilter
    pagination_class = DefaultPagination

    @action(detail=False, methods=["GET"])
    def summary(self, request):
        """
        Get a summary of all tickets
        """
        ticket_summary = Ticket.objects.get_summary(user_id=request.user.id)
        if request.method == "GET":
            return Response(ticket_summary)


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
