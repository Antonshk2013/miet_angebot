from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from src.commons.choices import (
    CountRumsChoice,
    DeclinedTypeChoice,
    ApartmentTypeChoice,
)

user_model = get_user_model()

class Listing(models.Model):
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    location = models.CharField(
        max_length=100
    )
    is_active = models.BooleanField(
        default=True
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    rooms_count = models.CharField(
        max_length=100,
        choices=CountRumsChoice.choices()
    )
    apartment_type = models.CharField(
        max_length=100,
        choices=ApartmentTypeChoice.choices()
    )
    cancellation_policy = models.CharField(
        max_length=100,
        choices=DeclinedTypeChoice.choices()
    )
    author = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.id} {self.title}"