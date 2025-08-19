from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from src.miet_angebot.models import Comment, Listing


@receiver(post_save, sender=Comment)
def update_listing_rating(sender, instance, created, **kwargs):
    if created:
        listing = instance.listing
        avg_rating = listing.comments.aggregate(avg=Avg('rating'))['avg'] or 0
        listing.rating = avg_rating
        listing.save(update_fields=['rating'])