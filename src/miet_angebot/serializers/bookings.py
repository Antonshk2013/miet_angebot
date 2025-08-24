from django.db.models import Q
from django.utils import timezone

from rest_framework import serializers

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers.comments import RetrieveCommentSerializer
from src.miet_angebot.serializers.listings import GuestRetrieveListingSerializer
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
    listing = GuestRetrieveListingSerializer()
    comments = RetrieveCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'date_start',
            'date_end',
            'status',
            'comments',
        ]

    def get_comments(self, obj):
        comments = obj.comments.all()
        return comments

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

        include_statuses = [
            BookingStatusChoice.created.value,
            BookingStatusChoice.accepted.value
        ]
        exclude_statuses = [
            BookingStatusChoice.declined.value,
            BookingStatusChoice.canceled.value
        ]
        bookings = Booking.objects.filter(
            listing=listing,
            status__in=include_statuses
        ).exclude(
            status__in=exclude_statuses
        ).filter(
            Q(date_start__lte=date_start, date_end__gte=date_start) |
            Q(date_start__lte=date_end, date_end__gte=date_end)
        )
        if bookings.exists():
            raise serializers.ValidationError("Listing is already exists.")
        return data