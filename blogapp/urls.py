from django.urls import path
from . import views
from .views import (
    PostListAPIView, PostDetailAPIView,
    CommentListAPIView, CategoryListAPIView
)

urlpatterns = [
    # Main views
    path('', views.blog_home, name='blog_home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('archives/', views.post_archive, name='post_archive'),
    path('upcoming/', views.upcoming_posts, name='upcoming_posts'),
    path('register/', views.register_user, name='register'),

    # API views
    path('api/latest-posts/', views.api_latest_posts, name='api_latest_posts'),
    path('api/posts-by-category/<slug:category_slug>/', views.api_posts_by_category, name='api_posts_by_category'),
    path('api/posts/', PostListAPIView.as_view(), name='api-posts'),
    path('api/posts/<slug:slug>/', PostDetailAPIView.as_view(), name='api-post-detail'),
    path('api/comments/', CommentListAPIView.as_view(), name='api-comments'),
    path('api/categories/', CategoryListAPIView.as_view(), name='api-categories'),
]
