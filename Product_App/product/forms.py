__author__ = 'krop'
from django import forms

from .models import Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop('entry')   # the blog entry instance
        super().__init__(*args, **kwargs)

    def save(self):
        comment = super().save(commit=False)
        comment.entry = self.entry
        comment.save()
        return comment