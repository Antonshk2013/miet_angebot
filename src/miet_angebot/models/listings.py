from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from src.commons.choices import (
    CountRumsChoice,
    DeclinedTypeChoice,
    ApartmentTypeChoice,
)
from src.commons.mixins import ModelCreatedUpdatedMixin

user_model = get_user_model()

class Listing(ModelCreatedUpdatedMixin, models.Model):
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

    @property
    def short_description(self, len_discr = 12):
        if len(self.description)>len_discr:
            return f"{self.description[:len_discr]}..."
        return self.description[:len_discr+3]

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id} {self.title}"