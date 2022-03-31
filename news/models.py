from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Max
from django.shortcuts import reverse


class Author(models.Model):
    full_name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.full_name.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name_cat = models.CharField(max_length=62, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return f'{self.name_cat}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return f'category/{self.pk}'


class Post(models.Model):
    article = 'Article'
    news = 'News'
    choice = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор')  # , related_name='posts')
    choices = models.CharField(max_length=7, choices=choice, default=article, verbose_name='Тип')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата')  # (blank=True, null=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(max_length=255, verbose_name='Текст новости')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    # url = models.URLField(verbose_name='Адрес')
    url = models.CharField(max_length=512, verbose_name='Адрес')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return f'{self.text}'
        return f'{self.text[124]}...'

    def __str__(self):
        return f'{self.title}: {self.text}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category}: {self.post}'


class CategorySubscribers(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # subscribers = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Статья')  # , related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # , related_name='user')
    text = models.TextField(verbose_name='Текст комментария')
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
