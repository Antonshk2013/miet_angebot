from rest_framework import serializers

from src.miet_angebot.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing