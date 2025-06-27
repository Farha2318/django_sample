from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post
from .forms import PostForm, CommentForm

def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator = Paginator(posts.order_by('-published_date'), 5)  # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blogapp/post_list.html', {
        'posts': posts,
        'query': query,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-created_at')
    form = CommentForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('post_detail', pk=pk)

    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blogapp/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blogapp/post_confirm_delete.html', {'post': post})