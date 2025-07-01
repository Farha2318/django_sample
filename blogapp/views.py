from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def blog_home(request):
    categories = Category.objects.prefetch_related('posts')
    return render(request, 'blogapp/home.html', {'categories': categories})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blogapp/post_detail.html', {'post': post})

# Optional dummy views
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())  # Redirect to post detail
    else:
        form = PostForm()  # ✅ this was missing its return

    # ✅ This line was missing before → return an HttpResponse for GET request
    return render(request, 'blogapp/post_form.html', {'form': form})

def post_create(request): pass
def post_edit(request, pk): pass
def post_delete(request, pk): pass
def post_archive(request): pass
def upcoming_posts(request):
    from django.utils import timezone
    upcoming = Post.objects.filter(is_scheduled=True, publish_on__gt=timezone.now()).order_by('publish_on')
    return render(request, 'blogapp/upcoming_posts.html', {'upcoming': upcoming})
