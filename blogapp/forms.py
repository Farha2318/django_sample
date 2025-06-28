from django import forms
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):
    """
    Form for creating or editing blog posts, including tags.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'author_name', 'image', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'content': forms.Textarea(attrs={'rows': 6}),
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

