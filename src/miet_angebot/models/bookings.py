from django.db import models
from django.contrib.auth import get_user_model

from src.miet_angebot.models.listings import Listing
from src.commons.choices import BookingStatusChoice
from src.commons.mixins import ModelCreatedUpdatedMixin


user_model = get_user_model()

class Booking(ModelCreatedUpdatedMixin, models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    date_start = models.DateField()
    date_end = models.DateField()
    author = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    status = models.CharField(
        max_length=100,
        choices=BookingStatusChoice.choices,
        null=True,
    )

    class Meta:
        permissions = [
            ("can_decline_booking", "Can decline booking"),
            ("can_cancel_booking", "Can cansel booking"),
            ("can_accept_booking", "Can accept booking"),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.date_start} {self.date_end}"