from django.db.models.signals import post_save
from django.dispatch import receiver

from src.miet_angebot.models import CounterListing

@receiver(post_save, sender=CounterListing)
def update_count_views(sender, instance, created, **kwargs):
    if created:
        listing = instance.listing
        count = listing.counter_listings.count()
        listing.count_views = count or 0
        listing.save(update_fields=["count_views"])