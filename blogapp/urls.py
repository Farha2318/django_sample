from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # Example: list of posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # View a single post
    path('post/new/', views.post_create, name='post_create'),  # Create a new post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # Edit a post
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),  # Delete a post
]