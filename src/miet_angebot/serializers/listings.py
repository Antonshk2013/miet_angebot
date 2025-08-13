from rest_framework import serializers

from src.miet_angebot.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'description',
            'location',
            'is_active',
            'price_per_day',
            'rooms_count',
            'apartment_type',
            'cancellation_policy',
        ]