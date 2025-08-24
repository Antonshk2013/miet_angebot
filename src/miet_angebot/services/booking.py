from django.utils import timezone
from src.commons.choices import BookingStatusChoice
from src.miet_angebot.models import Booking
from src.commons.choices import DeclinedTypeChoice



class BookingService:

    @staticmethod
    def is_to_canceled(instance: Booking):
        date_diff = instance.date_start - timezone.now().date()
        can_policy = instance.listing.cancellation_policy
        if can_policy == DeclinedTypeChoice.ever.value:
            return True
        elif can_policy== DeclinedTypeChoice.newer.value:
            return False
        elif can_policy == DeclinedTypeChoice.woche.value and date_diff.days > 7:
            return True
        elif can_policy == DeclinedTypeChoice.month.value and date_diff.days > 30:
            return True
        else:
            return False



