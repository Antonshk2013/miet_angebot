from django.db import models
from django.contrib.auth import get_user_model

from src.commons.base_model import BaseModel
from src.miet_angebot.models import Listing

user_model = get_user_model()

class CounterListing(BaseModel):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='counter_listings')
    author = models.ForeignKey(user_model, on_delete=models.CASCADE)