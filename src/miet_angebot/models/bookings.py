from django.db import models
from django.contrib.auth import get_user_model

from src.miet_angebot.models.listings import Listing

user_model = get_user_model()

class Booking(models.Model):
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
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.id} {self.date_start} {self.date_end}"