import random
import string

from django.db import models


class TicketNumberField(models.CharField):
    """
    Custom field to generate a ticket number
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("unique", True)
        kwargs.setdefault("default", self.generate_ticket_number)
        super().__init__(*args, **kwargs)

    def generate_ticket_number(self):
        """
        Generate a random ticket number
        """
        return "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=self.max_length,
            ),
        )
