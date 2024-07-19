from django import forms

from apps.home.models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
