from django.contrib import admin

from src.miet_angebot.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "listing",
        "author",
        "date_start",
        "date_end",
    )
    list_filter = (
        "date_start",
        "date_end",
        "listing__location",
    )
    search_fields = (
        "listing__title",
        "listing__location",
        "author__username",
    )
    ordering = ("-date_start",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")


