from rest_framework import serializers

from src.miet_angebot.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = [
            'id',
            'listing_title',
            'date_start',
            'date_end',
            'author',
        ]

    def get_listing_title(self, obj):
        return obj.listing.title