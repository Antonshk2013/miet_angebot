from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

user_model = get_user_model()

class UserApiSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(
            queryset=user_model.objects.all()
        )
    ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=user_model.objects.all()
        )
    ]
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True
    )

    role = serializers.ChoiceField(
        choices=[("guest", "Guest"), ("host", "Host")],
        write_only=True,
        required=True
    )

    class Meta:
        model = user_model
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop('password')
        user = user_model(**validated_data)
        user.set_password(password)  # хэшируем пароль
        user.save()

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        return user