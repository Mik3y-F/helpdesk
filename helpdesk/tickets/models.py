# Create your models here.

import datetime

from django.conf import settings
from django.db import models

from .fields import TicketNumberField


class TicketQuerySet(models.QuerySet):
    def safe_count(self, tickets_queryset: models.QuerySet):
        if tickets_queryset is None:
            return 0
        return tickets_queryset.count()

    def annotate_latest_status(self):
        latest_status = TicketStatus.objects.filter(
            ticket_id=models.OuterRef("pk"),
        ).order_by("-created_at")

        return self.annotate(
            latest_status=models.Subquery(latest_status.values("status")[:1]),
        )

    def due_today(self):
        return self.filter(due_date__date=datetime.date.today())

    def assigned_to_me(self, user_id):
        return self.filter(assigned_to=user_id)

    def unassigned(self):
        return self.filter(assigned_to__isnull=True)

    def overdue(self):
        return self.filter(due_date__lt=datetime.date.today())

    def open(self):
        return self.annotate_latest_status().filter(latest_status__in=["N", "IP"])

    def closed(self):
        self.annotate_latest_status().filter(latest_status__in=["R", "C"])

    def assigned_to_others(self, user_id):
        return self.filter(assigned_to__isnull=False).exclude(
            assigned_to=user_id,
        )

    def get_summary(self, user_id):
        return [
            {
                "display_name": "Unassigned",
                "system_name": "unassigned",
                "count": self.safe_count(self.unassigned()),
            },
            {
                "display_name": "Due Today",
                "system_name": "due_today",
                "count": self.safe_count(self.due_today()),
            },
            {
                "display_name": "Assigned to Me",
                "system_name": "assigned_to_me",
                "count": self.safe_count(self.assigned_to_me(user_id)),
            },
            {
                "display_name": "Overdue",
                "system_name": "overdue",
                "count": self.safe_count(self.overdue()),
            },
            {
                "display_name": "Open",
                "system_name": "open",
                "count": self.safe_count(self.open()),
            },
            {
                "display_name": "Closed",
                "system_name": "closed",
                "count": self.safe_count(self.closed()),
            },
            {
                "display_name": "Assigned to Others",
                "system_name": "assigned_to_others",
                "count": self.safe_count(self.assigned_to_others(user_id)),
            },
            {
                "display_name": "Everything",
                "system_name": "everything",
                "count": self.safe_count(self.all()),
            },
        ]


class TicketManager(models.Manager):
    def get_queryset(self):
        return TicketQuerySet(self.model, using=self._db)

    def due_today(self):
        return self.get_queryset().due_today()

    def assigned_to_me(self, user_id):
        return self.get_queryset().assigned_to_me(user_id)

    def unassigned(self):
        return self.get_queryset().unassigned()

    def overdue(self):
        return self.get_queryset().overdue()

    def open(self):
        return self.get_queryset().open()

    def closed(self):
        return self.get_queryset().closed()

    def assigned_to_others(self, user_id):
        return self.get_queryset().assigned_to_others(user_id)

    def get_summary(self, user_id):
        return self.get_queryset().get_summary(user_id)


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
    due_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TicketManager()

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
