from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from src.miet_angebot.models import Listing
from src.commons.mixins import ModelCreatedUpdatedMixin

user_model = get_user_model()

class Comment(ModelCreatedUpdatedMixin, models.Model):
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)]
    )
    author = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
