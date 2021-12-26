from django.forms import ModelForm
from .models import Post, Comment
from datetime import datetime
from django.forms import Form
from django.forms import CharField, EmailField, IntegerField
from django.forms import DateTimeField


class PostForm(ModelForm):
    # author = User.objects.get(id=18)
    # date_time = DateTimeField(widget=DateTimeInput, input_formats='')
    # date_time = datetime.now()
    # print(date_time)

    class Meta:
        model = Post
        fields = ['author',
                  'choices',
                  'category',
                  'title',
                  'text']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
