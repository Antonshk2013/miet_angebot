from rest_framework import serializers

from src.miet_angebot.models import Listing


class GuestListListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title',
            'short_description',
            'location',
            'price_per_day',
            'rooms_count',
            'apartment_type',
        ]

class GuestRetrieveListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'location',
            'price_per_day',
            'rooms_count',
            'apartment_type',
            'cancellation_policy',
        ]

class HostListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'location',
            'is_active',
            'price_per_day',
            'rooms_count',
            'apartment_type',
            'cancellation_policy',
        ]

class HostRetrieveListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'location',
            'is_active',
            'price_per_day',
            'rooms_count',
            'apartment_type',
            'cancellation_policy',
        ]

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