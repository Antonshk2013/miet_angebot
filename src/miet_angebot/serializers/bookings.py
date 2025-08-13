from rest_framework import serializers

from src.miet_angebot.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking