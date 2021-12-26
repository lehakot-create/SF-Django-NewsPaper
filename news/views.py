from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category
from django.contrib.auth.models import User
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from datetime import datetime


class NewsList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object.author_id
        _id = self.object.id
        # print(Comment.objects.filter(post_id=_id).values('user_id'))
        if Comment.objects.filter(post_id=_id).exists():
            context['comment'] = Comment.objects.filter(post_id=_id).values('text', 'user')
            # all_id = Comment.objects.filter(post_id='1').values('id')
            # for _id in all_id:
            #     context['comment'] = Comment.objects.get(id=_id['id']).user
        else:
            context['comment'] = '-'
        # print(context)
        return context

    # def post(self, request, *args, **kwargs):
    #     print(request)

        # comment_text = request.POST['name']
        # # print(comment_text)
        # comment = Comment.objects.create(post=self.object,
        #                                  user=User.objects.get(id=18),
        #                                  text=comment_text)
        # comment.save()
        # return super().get(request, *args, **kwargs)

        # Comment.objects.create(post=post, user=user, text='Афтар жжот')


# class CommentCreateView(CreateView):
#     template_name = 'news/post.html'
#     form_class = CommentForm
#     success_url = '/news/'


class CommentDetail(DetailView):
    model = Comment
    template_name = 'news/post.html'
    context_object_name = 'comment'


class Search(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    paginate_by = 10
    success_url = 'news/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
        # paginator = Paginator(context, 10)
        # print(context)
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'category'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _id = self.kwargs.get('pk')
        context['category'] = Category.objects.get(id=_id)
        c = Category.objects.get(id=_id)
        context['posts'] = Post.objects.filter(category=c)
        print(context)
        return context


class PostCreateView(CreateView):
    template_name = 'news/add_post.html'
    form_class = PostForm

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     # form.data['date_time'] = datetime.now()
    #     # # print(form)
    #     # print(form.data)
    #
    #     if form.is_valid():
    #         form.save()
    #
    #     return super().get(request, *args, **kwargs)


class PostUpdateView(UpdateView):
    template_name = 'news/update_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/delete_post.html'
    queryset = Post.objects.all()
    success_url = '/news/'