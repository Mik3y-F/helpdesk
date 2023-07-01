from django.contrib import admin

from .models import Ticket, TicketStatus


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin class for the Ticket model
    """

    pass


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    """
    Admin class for the TicketStatus model
    """

    pass
