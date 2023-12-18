from django import forms
from .models import Post
from .models import Author, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories", "tags"]
