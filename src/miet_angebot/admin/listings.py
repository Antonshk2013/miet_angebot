from django.contrib import admin

from src.miet_angebot.models import Listing


@admin.register(Listing)
class ListingsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "location",
        "price_per_day",
        "rooms_count",
        "apartment_type",
        "cancellation_policy",
        "is_active",
        "author",
    )
    list_filter = (
        "is_active",
        "rooms_count",
        "apartment_type",
        "cancellation_policy",
        "author",
    )
    search_fields = (
        "title",
        "description",
        "location",
        "author__username",
    )
    ordering = ("-is_active", "price_per_day")
    list_editable = ("is_active",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")


