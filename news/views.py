from django.views.generic import ListView, DetailView
from .models import Post, Comment, Category
from django.contrib.auth.models import User


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object.author_id
        _id = self.object.id
        print(Comment.objects.filter(post_id=_id).values('user_id'))
        if Comment.objects.filter(post_id=_id).exists():
            context['comment'] = Comment.objects.filter(post_id=_id).values('text')
        else:
            context['comment'] = '-'
        print(context)
        return context


class CommentDetail(DetailView):
    model = Comment
    template_name = 'post.html'
    context_object_name = 'comment'
