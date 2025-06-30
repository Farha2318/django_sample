from django import forms
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):
    """
    Form for creating or editing blog posts, including tags and scheduling.
    """
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author_name',
            'image',
            'tags',
            'is_scheduled',
            'publish_on',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
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