from django.contrib import admin
from django.db.models import ImageField
from django.utils.html import format_html

from . import utils
from .models import Notification, Post, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "phone",
        "date_joined",
        "avatar",
    )
    search_fields = ("username", "first_name", "last_name", "phone")
    list_filter = ("date_joined",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_content",
        "author",
        "likes_count",
        "created_at",
        "updated_at",
    )
    search_fields = ("content", "author__username")
    list_filter = ("created_at", "author")

    formfield_overrides = {
        ImageField: {"widget": utils.ImagePreviewAdminWidget},
    }

    def display_content(self, obj):
        if obj.content:
            return format_html(
                f"<img src=\"{obj.content.url.replace('minio', 'localhost')}\" width=\"200\" height=\"150\" style=\"border-radius: 5px;\">"
            )
        else:
            return "No image available"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("type", "post", "liked_by")
    search_fields = ("type", "post__content", "liked_by__username")
    list_filter = ("type",)
