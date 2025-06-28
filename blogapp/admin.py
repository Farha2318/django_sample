from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'published_date', 'display_tags', 'image_preview')
    search_fields = ('title', 'content', 'author_name')
    list_filter = ('published_date', 'tags')

    def display_tags(self, obj):
        """Display tags as comma-separated names in list view."""
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

    def image_preview(self, obj):
        """Show a small preview of the image in list view."""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    search_fields = ('name', 'message')
    list_filter = ('created_at', 'post')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)