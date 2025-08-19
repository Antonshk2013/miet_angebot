from django.template.defaulttags import comment
from rest_framework import serializers

from src.miet_angebot.models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'rating',
            'comment',
            'user',
            'listing'
        ]


class RetrieveCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'rating',
            'comment',
            'user_name',
        ]

    def get_username(self, obj):
        return obj.user.username