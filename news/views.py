import datetime
import pytz
from datetime import datetime
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import Http404
from django.core.cache import cache
from rest_framework import generics, permissions, status, mixins
from rest_framework.response import Response

from .tasks import send_email
from .filters import PostFilter
from .forms import PostForm, CommentForm, UserProfileForm
from .models import Post, Comment, Category, Author
from .serializers import NewsSerializer


class NewsList(ListView):
    # permission_required = ('news.view_post')
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class NewsDetailView(TemplateView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = cache.get(f'post-{kwargs.get("pk")}', None)
        if not post:
            post = Post.objects.get(id=kwargs.get('pk'))
            cache.set(f'post-{kwargs.get("pk")}', post)
        comment = Comment.objects.filter(post_id=kwargs.get('pk'))\
            .values('text', 'user__username')
        form = CommentForm()

        try:
            id = post.category.values('id')[0]['id']
        except IndexError:
            raise Http404('Не указана категория новости')

        c = Category.objects.get(id=id)
        try:
            uid = User.objects.get(username=request.user).id
            s = c.subscribers.filter(id=uid).exists()
            if s:
                s = c.subscribers.filter(id=uid)[0].username
                if s == request.user.username:
                    subscriber = True
            else:
                subscriber = False
        except User.DoesNotExist:
            subscriber = False

        return render(request, 'news/post.html', {'post': post,
                                                  'comment': comment,
                                                  'form': form,
                                                  'subscriber': subscriber})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data
            post = Post.objects.get(id=kwargs.get('pk'))
            Comment.objects.create(post=post,
                                   user=request.user,
                                   text=text['text'])
            url = post.get_absolute_url()
            return redirect(url)
        raise Http404('Неверные данные')


@login_required
def subscribe(request, pk):
    if request.method == 'GET':
        u = request.user
        p = Post.objects.get(id=pk).category.values('id')[0]['id']
        c = Category.objects.get(id=p)
        c.subscribers.add(u)

    send_email.apply_async(kwargs={'user_id': request.user.id,
                            'pk': pk,
                            'category_id': c.id})

    url = Post.objects.get(id=pk).get_absolute_url()
    return redirect(url)


@login_required
def unsubscribe(request, pk):
    if request.method == 'GET':
        u = request.user
        p = Post.objects.get(id=pk).category.values('id')[0]['id']
        c = Category.objects.get(id=p)
        c.subscribers.remove(u)
    url = Post.objects.get(id=pk).get_absolute_url()
    return redirect(url)


class Search(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'posts'
    paginate_by = 3
    ordering = ['-date_time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())
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
        context['posts'] = Post.objects.filter(category=c).order_by('-date_time')
        return context


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'news/add_post.html'
    form_class = PostForm
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.author = Author.objects.get(full_name_id=self.request.user.id)
        return super(PostCreateView, self).form_valid(form)

    def get(self, request):
        if Post.objects.filter(author=Author.objects.get(full_name_id=self.request.user.id),
                                          date_time__contains=datetime.today().date()).count() > 2:
            raise Http404('Лимит на создание новостей на сегодня превышен')
        return super(PostCreateView, self).get(self.request)


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'news/update_post.html'
    form_class = PostForm
    success_url = reverse_lazy('news_list')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'news/delete_post.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news_list')


@login_required
def upgrade(request):
    user = request.user
    group = Group.objects.get(name='authors')
    group.user_set.add(user)
    try:
        Author.objects.get(full_name=User.objects.get(id=user.id))
    except Author.DoesNotExist:
        Author.objects.create(full_name=User.objects.get(id=user.id))
    return redirect('news_list')


class ProfileDetailView(UpdateView):
    model = User
    template_name = 'news/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        if self.request.user.id == self.kwargs.get('pk'):
            context = super().get_context_data(**kwargs)
            context['profile'] = User.objects.get(id=self.kwargs.get('pk'))
        else:
            raise Http404('Данная страница вам не доступна')
        return context


# class NewsApi(generics.ListCreateAPIView):
#     queryset = Post.objects.all().filter(choices='News')
#     serializer_class = NewsSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def post(self, request, *args, **kwargs):
#         author = Author.objects.get(full_name_id=request.user.id)
#         request.data['author'] = author.id
#         serializer = NewsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsApi(generics.ListCreateAPIView):
    queryset = Post.objects.all().filter(choices='News')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(full_name_id=request.user.id)
        request.data['author'] = author.id
        request.data['choices'] = 'News'
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().filter(choices='News')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, pk, format=None):
        news = self.get_object()
        author = Author.objects.get(full_name_id=request.user.id)
        request.data['author'] = author.id
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesApi(generics.ListCreateAPIView):
    queryset = Post.objects.all().filter(choices='Article')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        author = Author.objects.get(full_name_id=request.user.id)
        request.data['author'] = author.id
        request.data['choices'] = 'Article'
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticlesApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().filter(choices='Article')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, pk, format=None):
        news = self.get_object()
        author = Author.objects.get(full_name_id=request.user.id)
        request.data['author'] = author.id
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)