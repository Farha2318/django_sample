from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import generics
from .models import Post, Comment, Category
from .serializers import PostSerializer, CommentSerializer, CategorySerializer
from .models import Category, Post
from .forms import PostForm  
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test


# ✅ Helper: allow only admin (staff) users
def is_staff_user(user):
    return user.is_staff


def blog_home(request):
    categories = Category.objects.prefetch_related('posts')
    return render(request, 'blogapp/home.html', {'categories': categories})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blogapp/post_detail.html', {'post': post})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/post_list.html', {'posts': posts})


@staff_member_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('post_list')  # or use post.get_absolute_url() if defined
    else:
        form = PostForm()
    return render(request, 'blogapp/post_form.html', {'form': form})
def post_edit(request, pk):
    pass


def post_delete(request, pk):
    pass


def post_archive(request):
    pass


def upcoming_posts(request):
    upcoming = Post.objects.filter(
        is_scheduled=True,
        publish_on__gt=timezone.now()
    ).order_by('publish_on')
    return render(request, 'blogapp/upcoming_posts.html', {'upcoming': upcoming})


# ✅ API: Latest 5 published posts
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@ratelimit(key='ip', rate='10/m', block=True)
def api_latest_posts(request):
    posts = Post.objects.filter(is_scheduled=False).order_by('-published_date')[:5]
    data = [
        {
            'title': post.title,
            'slug': post.slug,
            'published_date': post.published_date,
            'category': post.category.name if post.category else None
        }
        for post in posts
    ]
    return JsonResponse(data, safe=False)


# ✅ API: Posts by category
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@ratelimit(key='ip', rate='10/m', block=True)
def api_posts_by_category(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)

    posts = Post.objects.filter(category=category, is_scheduled=False).order_by('-published_date')
    data = [
        {
            'title': post.title,
            'slug': post.slug,
            'published_date': post.published_date,
        }
        for post in posts
    ]
    return JsonResponse(data, safe=False)


# ✅ User registration view
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Assumes 'login' URL name exists
    else:
        form = UserCreationForm()
    return render(request, "blogapp/register.html", {"form": form})

# Posts
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(is_scheduled=False)
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

# Comments
class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# Categories
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


