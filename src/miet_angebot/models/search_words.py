from django.db import models

from src.commons.base_model import BaseModel


class SearchWords(BaseModel):
    word = models.CharField(
        max_length=255,
        unique=True
    )
    counter = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:
            existing = SearchWords.objects.filter(word=self.word).first()
            if existing:
                existing.counter += 1
                existing.save(update_fields=["counter"])
                return
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-counter']