import os
import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from faker import Faker
from random import choice, uniform
from decimal import Decimal


from src.miet_angebot.models import Listing
from src.commons.choices import (
    CountRumsChoice,
    ApartmentTypeChoice,
    DeclinedTypeChoice
)
from src.miet_angebot.serializers import ListingSerializer

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"Superuser {username} already exists")

if not Group.objects.exists():
    print(f"Creating group host")
    group_host = Group.objects.create(name="host")
    group_host.save()
    print(f"Creating group guest")
    group_host = Group.objects.create(name="guest")
    group_host.save()

def create_user_with_group(group_name):
    user_range = range(3)

    for i in user_range:
        user_data = f"{group_name}{i}"
        user=User.objects.create_user(
            username=user_data,
            email=user_data+"@test,com",
            password=user_data+user_data)
        user.groups.add(Group.objects.get(name=group_name))
        user.save()
if not User.objects.filter(groups__name="host").exists():
    create_user_with_group("host")
if not User.objects.filter(groups__name="guest").exists():
    create_user_with_group("guest")

if not Listing.objects.exists():
    fake = Faker("de_DE")
    users = list(User.objects.filter(groups__name="host"))
    mecklenburg_vorpommern_cities = [
        "Rostock",
        "Schwerin",
        "Neubrandenburg",
        "Stralsund",
        "Greifswald",
        "Wismar",
        "Güstrow",
        "Waren (Müritz)",
        "Parchim",
        "Anklam",
        "Ludwigslust",
        "Ribnitz-Damgarten",
        "Bergen auf Rügen",
        "Demmin",
        "Ueckermünde",
        "Teterow",
        "Grimmen",
        "Malchin",
        "Bad Doberan",
        "Putbus",
    ]

    for i in range(60):
        land = "Mecklenburg-Vorpommern"
        city = choice(mecklenburg_vorpommern_cities)


        data = {
            "title": fake.sentence(nb_words=4),
            "description": fake.paragraph(nb_sentences=5),
            "location": f"{land}, {city}",
            "is_active": choice([True, False]),
            "price_per_day": Decimal(str(round(uniform(30, 150), 2))),
            "rooms_count": choice([c[0] for c in CountRumsChoice.choices()]),
            "apartment_type": choice([c[0] for c in ApartmentTypeChoice.choices()]),
            "cancellation_policy": choice([c[0] for c in DeclinedTypeChoice.choices()]),
        }


        serializer = ListingSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(author=choice(users))
            serializer.save()
        except ValidationError as e:
            print(f"Ошибка в {i}: {e}")
