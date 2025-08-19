from django.template.defaulttags import comment
from rest_framework import serializers

from src.miet_angebot.models import Comment


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'rating',
            'comment',
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

    def get_user_name(self, obj):
        return obj.author.username

    #TODO
    #Сколько угодно может ставить комментарий
    #Проверяем по дате выезда