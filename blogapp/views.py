from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Tag
from .forms import PostForm, CommentForm


def post_list(request):
    """
    Display a list of posts with optional search and tag filtering.
    Supports pagination.
    """
    query = request.GET.get('q')
    tag_id = request.GET.get('tag')
    posts = Post.objects.all()

    # Filter by search query
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    # Filter by selected tag
    if tag_id:
        posts = posts.filter(tags__id=tag_id)

    # Paginate the results
    paginator = Paginator(posts.order_by('-published_date'), 5)  # 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    tags = Tag.objects.all()

    return render(request, 'blogapp/post_list.html', {
        'posts': posts,
        'query': query,
        'tags': tags,
        'selected_tag': int(tag_id) if tag_id else None,
    })


def post_detail(request, pk):
    """
    Display details of a single post, including comments.
    Handles new comment submission.
    """
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
    """
    Create a new blog post.
    """
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        form.save_m2m()  # Save tags
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})


def post_edit(request, pk):
    """
    Edit an existing blog post.
    """
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        form.save_m2m()  # Save updated tags
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blogapp/post_form.html', {'form': form})


def post_delete(request, pk):
    """
    Delete a blog post with confirmation.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blogapp/post_confirm_delete.html', {'post': post})