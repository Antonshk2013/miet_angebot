from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Count

from src.miet_angebot.models import Comment, Listing


@receiver(post_save, sender=Comment)
def update_listing_rating(sender, instance, created, **kwargs):
    if created:
        listing = instance.listing
        agg = listing.comments.aggregate(
            avg=Avg("rating"),
            count_comments=Count("id")
        )
        listing.rating = agg.get("avg") or 0
        listing.count_comments = agg.get("count_comments") or 0
        listing.save(update_fields=["rating", "count_comments"])