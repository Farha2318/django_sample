from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'published_date')
    search_fields = ('title', 'content', 'author_name')
    list_filter = ('published_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    search_fields = ('name', 'message')
    list_filter = ('created_at', 'post')