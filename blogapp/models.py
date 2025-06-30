from django.db import models
from django.utils import timezone

class Tag(models.Model):
    """
    Custom tag model for categorizing blog posts.
    """
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Blog post model.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    # 🔹 New fields for scheduling
    is_scheduled = models.BooleanField(default=False)
    publish_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def is_published(self):
        """
        Returns True if the post is either not scheduled or scheduled and ready to be shown.
        """
        if self.is_scheduled:
            return self.publish_on and self.publish_on <= timezone.now()
        return True


class Comment(models.Model):
    """
    Comment model related to a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"