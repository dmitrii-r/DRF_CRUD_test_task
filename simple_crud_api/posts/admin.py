from django.contrib import admin

from posts.models import Post

EMPTY_VALUE_DISPLAY = "-пусто-"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "name", "created", "is_published")
    list_filter = ("author", "is_published")
    list_display_links = ("id", "name")
    empty_value_display = EMPTY_VALUE_DISPLAY
