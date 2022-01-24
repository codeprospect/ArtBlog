from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class  Meta:
        model = Post
        fields = ('author', 'title', 'content', 'date', 'image')

class PostSearchForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title')


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        # widgets = {
        #     'Name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'body': forms.TextArea(attrs={'class': 'form-control'}),
        # }
