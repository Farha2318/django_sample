from django.test import TestCase
from .models import Post, Comment, Category

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_string_representation(self):
        post = Post(title="Test Post", category=self.category)
        self.assertEqual(str(post), "Test Post")

    def test_post_creation_and_retrieval(self):
        post = Post.objects.create(
            title="Sample Post",
            content="This is a test post.",
            author_name="Farhana",
            category=self.category
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().title, "Sample Post")

class CommentModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Another Category", slug="another-category")
        self.post = Post.objects.create(
            title="Parent Post",
            content="Some content",
            author_name="Farhana",
            category=self.category
        )

    def test_string_representation(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Reader",
            message="Nice post!"
        )
        self.assertEqual(str(comment), "Comment by Reader on Parent Post")
