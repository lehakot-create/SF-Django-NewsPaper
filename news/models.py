from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Max


class Author(models.Model):
    full_name = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    # @staticmethod
    # def update_rating(author):
    #     rating_all_articles = author.posts.all().aggregate(Sum('rating'))['rating__sum']
    #
    #     c = Comment.objects.all()
    #     rating_all_comment = c.filter(user=author.full_name.id).values('rating').aggregate(Sum('rating'))['rating__sum']
    #
    #     rating_comment_to_article = 0
    #     p = Post.objects.filter(author=author)
    #     for el in p.values('id'):
    #         if Comment.objects.filter(post_id=el['id']).exists():
    #             rating_comment_to_article += Comment.objects.filter(post_id=el['id']).values('rating')[0]['rating']
    #
    #     rating = rating_all_articles * 3 + rating_all_comment + rating_comment_to_article
    #     author.rating = rating
    #     author.save()

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

    def __str__(self):
        return f'{self.name_cat}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    article = 'Article'
    news = 'News'
    choice = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор')  # , related_name='posts')
    choices = models.CharField(max_length=7, choices=choice, default=article, verbose_name='Тип')
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    text = models.TextField(max_length=255, verbose_name='Текст новости')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    url = models.URLField(verbose_name='Адрес')

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
        return f'{self.pk}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.category}: {self.post}'


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
