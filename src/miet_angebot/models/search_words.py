from django.db import models

from src.commons.base_model import BaseModel


class SearchWordsModel(BaseModel):
    word = models.CharField(
        max_length=255,
        unique=True
    )
    counter = models.PositiveIntegerField(default=1)