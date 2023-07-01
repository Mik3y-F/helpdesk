# Create your models here.

from django.conf import settings
from django.db import models

from .fields import TicketNumberField


class Ticket(models.Model):
    INCIDENT = "I"
    REQUEST = "R"

    TICKET_TYPE = [
        (INCIDENT, "Incident"),
        (REQUEST, "Request"),
    ]

    CRITICAL = "C"
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"

    PRIORITY = [
        (CRITICAL, "Critical"),
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    ticket_type = models.CharField(max_length=1, choices=TICKET_TYPE, default=INCIDENT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_to",
        null=True,
        blank=True,
    )

    ticket_number = TicketNumberField(max_length=8)
    priority = models.CharField(max_length=1, choices=PRIORITY, default=LOW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TicketStatus(models.Model):
    NEW = "N"
    IN_PROGRESS = "IP"
    RESOLVED = "R"
    CLOSED = "C"

    STATUS = [
        (NEW, "New"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
        (CLOSED, "Closed"),
    ]

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="statuses",
    )
    status = models.CharField(max_length=2, choices=STATUS, default=NEW)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.status}"

    class Meta:
        get_latest_by = "created_at"
