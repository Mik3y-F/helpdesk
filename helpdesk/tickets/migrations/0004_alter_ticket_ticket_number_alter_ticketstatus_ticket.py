# Generated by Django 4.1.9 on 2023-06-30 02:13

from django.db import migrations, models
import django.db.models.deletion
import helpdesk.tickets.fields


class Migration(migrations.Migration):
    dependencies = [
        ("tickets", "0003_alter_ticketstatus_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="ticket_number",
            field=helpdesk.tickets.fields.TicketNumberField(
                default=helpdesk.tickets.fields.TicketNumberField.generate_ticket_number, max_length=8, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="ticketstatus",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="statuses", to="tickets.ticket"
            ),
        ),
    ]