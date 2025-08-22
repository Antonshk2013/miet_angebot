from rest_framework import serializers
from datetime import date

from src.miet_angebot.models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'rating',
            'comment',
        ]

    def validate(self, attrs):
        view = self.context.get("view")
        booking = view.get_object()
        if booking is None:
            raise serializers.ValidationError("Booking is required for validation.")
        if date.today() < booking.date_end:
            raise serializers.ValidationError("You can leave a review starting from the check-out date.")
        return attrs


class RetrieveCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'rating',
            'comment',
            'user_name',
        ]

    def get_user_name(self, obj):
        return obj.author.username



