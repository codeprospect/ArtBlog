from django import forms
from .models import Post, Comment, Category

choices = Category.objects.all().values_list('name', 'name')
choice_list = []

for item in choices:
    choice_list.append(item)


class PostForm(forms.ModelForm):
    class  Meta:
        model = Post
        fields = ('title', 'category', 'snippet', 'content', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PostSearchForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title')


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
