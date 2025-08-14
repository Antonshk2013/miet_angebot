from datetime import timezone

from rest_framework import serializers

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers.listings import ListingSerializer
from src.commons.choices import BookingStatusChoice


class ListBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'date_start',
            'date_end',
            'status',
        ]

class RetrieveBookingSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'date_start',
            'date_end',
            'status',
        ]

class CreateUpdateBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            'listing',
            'date_start',
            'date_end',
            'status',
        ]

    def validate_listing(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This listing is not available for booking.")
        return value

    def validate_date_start(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return value

    def validate_date_end(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("End date cannot be in the past.")
        return value

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")

        if date_end <= date_start:
            raise serializers.ValidationError(
                {"date_end": "End date must be after start date."}
            )
        listing = data.get("listing")
        if Booking.objects.select_related("listing").filter(
            listing=listing,
            date_start__gte=date_start,
            date_end__lte=date_end,
            status__in=(
                    BookingStatusChoice.created.value,
                    BookingStatusChoice.accepted.value,
            )
        ).exists():
            raise serializers.ValidationError("Listing is already exists.")
        return data