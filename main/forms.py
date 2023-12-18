from django import forms
from .models import Post
from .models import Author, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "categories", "tags"]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user is not None:
            author = Author.objects.get(user=user)
            self.fields['categories'].queryset = author.chosen_categories.all()