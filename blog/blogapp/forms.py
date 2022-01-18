from django import forms
from .models import Post, Comment

class PostSearchForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
