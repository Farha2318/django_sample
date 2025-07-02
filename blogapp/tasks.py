from celery import shared_task
from django.utils import timezone
from .models import Post

@shared_task
def publish_scheduled_posts():
    now = timezone.now()
    scheduled_posts = Post.objects.filter(is_scheduled=True, publish_on__lte=now, is_published=False)
    
    for post in scheduled_posts:
        post.is_published = True  # ✅ Mark as published
        post.is_scheduled = False  # ✅ Unmark scheduled
        post.save()
        print(f"✅ Published: {post.title}")
    
    return f"Published {scheduled_posts.count()} post(s)"
