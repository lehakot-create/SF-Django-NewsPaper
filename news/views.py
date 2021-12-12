import datetime
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category, Author
from django.contrib.auth.models import User, Group
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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
        return context


def news_detail(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data
            Comment.objects.create(post=Post.objects.get(id=pk),
                                   user=request.user,
                                   text=text['text'])
    form = CommentForm()
    post = Post.objects.get(id=pk)
    comment = Comment.objects.filter(post_id=pk).values('text', 'user__username')

    # print('*' * 50)
    id = post.category.values('id')[0]['id']
    # print(f'id={id}')
    c = Category.objects.get(id=id)
    # print(f'c={c}')
    try:
        uid = User.objects.get(username=request.user).id
        # print(f'uid={uid}')
        s = c.subscribers.filter(id=uid).exists()
        # print(s)
        # print(request.user.username)
        # print('*' * 50)
        if s:
            s = c.subscribers.filter(id=uid)[0].username
            # print(s)
            if s == request.user.username:
                subscriber = True
        else:
            subscriber = False
    except User.DoesNotExist:
        subscriber = False

    return render(request, 'news/post.html', {'post': post, 'comment': comment, 'form': form, 'subscriber': subscriber})

@login_required
def subscribe(request, pk):
    if request.method == 'GET':
        u = request.user
        p = Post.objects.get(id=pk).category.values('id')[0]['id']
        c = Category.objects.get(id=p)
        c.subscribers.add(u)

    post = Post.objects.get(id=pk)
    html_content = render_to_string(
        'news/email.html',
        {'post': post, 'user': u, 'category': c}
    )
    msg = EmailMultiAlternatives(
        subject=f'{request.user}',
        body=post.text,
        from_email='alex85aleshka@yandex.ru',
        to=[u.email],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

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
        context['posts'] = Post.objects.filter(category=c)
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

