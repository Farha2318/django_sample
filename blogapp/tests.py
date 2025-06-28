from django.test import TestCase
from .models import Post, Comment

class PostModelTest(TestCase):
    def test_string_representation(self):
        post = Post(title="Test Post")
        self.assertEqual(str(post), "Test Post")

    def test_post_creation_and_retrieval(self):
        post = Post.objects.create(
            title="Sample Post",
            content="This is a test post.",
            author_name="Farhana"
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "Sample Post")

class CommentModelTest(TestCase):
    def test_string_representation(self):
        post = Post.objects.create(
            title="Parent Post",
            content="Some content",
            author_name="Farhana"
        )
        comment = Comment.objects.create(
            post=post,
            name="Reader",
            message="Nice post!"
        )
        self.assertEqual(str(comment), "Comment by Reader")