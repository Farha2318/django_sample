from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Post, Comment, Tag, Category

@admin.action(description="📢 Publish selected posts now")
def publish_now(modeladmin, request, queryset):
    now = timezone.now()
    queryset.filter(is_scheduled=True).update(publish_on=now)
    modeladmin.message_user(request, f"{queryset.count()} post(s) published now.")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'published_date', 'status_badge', 'display_tags', 'image_preview')
    search_fields = ('title', 'content', 'author_name')
    list_filter = ('published_date', 'tags', 'is_scheduled', 'category')
    fields = ('title', 'content', 'author_name', 'image', 'tags', 'category', 'is_scheduled', 'publish_on')
    actions = [publish_now]

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

    def status_badge(self, obj):
        if obj.is_scheduled and obj.publish_on and obj.publish_on > timezone.now():
            return format_html('<span style="color: orange;">Scheduled</span>')
        return format_html('<span style="color: green;">Published</span>')
    status_badge.short_description = 'Status'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    search_fields = ('name', 'message')
    list_filter = ('created_at', 'post')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
