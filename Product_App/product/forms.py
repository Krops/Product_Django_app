__author__ = 'krop'
from django.forms import ModelForm, Textarea, CharField



from .models import Post

class CommentForm(ModelForm):
    title = CharField(max_length=30,min_length=3, required=True)
    body = CharField(max_length=300,min_length=5, required=True,widget = Textarea(attrs={'cols': 24, 'rows': 5}),label='Enter the message')
    class Meta:
        model = Post
        fields = ['title', 'body']