# Generated by Django 4.1.9 on 2023-06-28 00:29

from django.db import migrations
import helpdesk.tickets.fields


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticket",
            name="upvotes",
        ),
        migrations.AlterField(
            model_name="ticket",
            name="ticket_number",
            field=helpdesk.tickets.fields.TicketNumberField(
                default=helpdesk.tickets.fields.TicketNumberField.generate_ticket_number, max_length=8, unique=True
            ),
        ),
    ]
