from django.contrib import admin

from src.miet_angebot.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # list_display = '__all__'
    ordering = ("-created_at",)
    list_per_page = 20
    readonly_fields = ("created_at", "updated_at")