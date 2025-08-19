from rest_framework import serializers
from src.miet_angebot.models import Listing


class GuestListListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'short_description',
            'location',
            'price_per_day',
            'rooms_count',
            'apartment_type',
            'rating',
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
            'rating',
        ]

class HostListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            'id',
            'title',
            'is_active',
            'price_per_day',
        ]

    def to_representation(self, instance):
        listing = super().to_representation(instance)
        listing['link'] = f"{self.context.get('request').build_absolute_uri()}{listing['id']}"
        return listing

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