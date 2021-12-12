from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class UserRating(models.Model):
    rating = models.IntegerField(User, default=0)


class Author(models.Model):
    full_name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    @staticmethod
    def update_rating(author):
        rating_all_articles = author.posts.all().aggregate(Sum('rating'))['rating__sum']

        c = Comment.objects.all()
        rating_all_comment = c.filter(user=author.full_name.id).values('rating').aggregate(Sum('rating'))['rating__sum']

        rating_comment_to_article = 0
        p = Post.objects.filter(author=author)
        for el in p.values('id'):
            if Comment.objects.filter(post_id=el['id']).exists():
                rating_comment_to_article += Comment.objects.filter(post_id=el['id']).values('rating')[0]['rating']

        rating = rating_all_articles * 3 + rating_all_comment + rating_comment_to_article
        author.rating = rating
        author.save()


class Category(models.Model):
    name_cat = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'Article'
    news = 'News'
    choice = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    choices = models.CharField(max_length=7, choices=choice, default=article)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=255)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
