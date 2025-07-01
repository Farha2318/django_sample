from django import forms
from .models import Post, Comment, Tag, Category

class PostForm(forms.ModelForm):
    """
    Form for creating or editing blog posts, including tags, category, and scheduling.
    """
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author_name',
            'image',
            'tags',
            'category',       # ✅ Added category field
            'is_scheduled',
            'publish_on',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'category': forms.Select(),  # Optional: customize with a styled dropdown
            'content': forms.Textarea(attrs={'rows': 6}),
            'publish_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    """
    Form for submitting comments on a post.
    """
    class Meta:
        model = Comment
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }