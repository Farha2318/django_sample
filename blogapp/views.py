from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from .models import Category, Post
from .forms import PostForm  # Assuming you have a PostForm defined

def blog_home(request):
    categories = Category.objects.prefetch_related('posts')
    return render(request, 'blogapp/home.html', {'categories': categories})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blogapp/post_detail.html', {'post': post})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blogapp/post_form.html', {'form': form})

def post_edit(request, pk): pass
def post_delete(request, pk): pass
def post_archive(request): pass

def upcoming_posts(request):
    upcoming = Post.objects.filter(
        is_scheduled=True,
        publish_on__gt=timezone.now()
    ).order_by('publish_on')
    return render(request, 'blogapp/upcoming_posts.html', {'upcoming': upcoming})

# ✅ API: Latest 5 published posts
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
