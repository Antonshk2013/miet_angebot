from src.commons.choices.base import BaseChoice

class BookingStatusChoice(BaseChoice):
    created = "created"
    updated = "updated"
    declined = "declined"
    canceled = "canceled"