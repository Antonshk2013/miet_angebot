from src.commons.choices.base import BaseChoice

class BookingStatusChoice(BaseChoice):
    created = "created"
    declined = "declined"
    canceled = "canceled"
    accepted = "accepted"