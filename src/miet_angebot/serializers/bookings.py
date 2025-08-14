from rest_framework import serializers

from src.miet_angebot.models import Booking
from src.miet_angebot.serializers.listings import ListingSerializer


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

class CreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'listing',
            'date_start',
            'date_end',
            'status',
        ]
