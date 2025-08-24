from rest_framework import serializers

from src.miet_angebot.models import SearchWords

class SearchWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWords
        fields = [
            'word',
            'counter'
        ]
