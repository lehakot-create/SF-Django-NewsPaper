from news.models import *


1
User.objects.create_user('bob')
User.objects.create_user('jack')

2
Author.objects.create(full_name=User.objects.all()[0])
Author.objects.create(full_name=User.objects.all()[1])

3
Category.objects.create(name_cat='Экономика')
Category.objects.create(name_cat='Криминал')
Category.objects.create(name_cat='Политика')
Category.objects.create(name_cat='Юмор')

4 и 5
a = Author.objects.all()[0]
cat = Category.objects.all()[0]
post = Post.objects.create(author=a, choices='Article',title='ЦБ повысил ставку',text='Сегодня Центральный Банк РФ повысил ключевую ставку до 360%')
post.category.add(cat)

a = Author.objects.all()[0]
cat = Category.objects.all()[1]
post = Post.objects.create(author=a, choices='News',title='Программа максимум:  показать все что скрыто', text='Внимание! Внимание! Сегодня под мостом нашли Гитлера с хвостом')
post.category.add(cat)

a = Author.objects.all()[1]
cat = Category.objects.all()[3]
post = Post.objects.create(author=a, choices='Article',title='Анекдот', text='Колобок повесился. Буратино утопился.')
post.category.add(cat)
cat2 = Category.objects.all()[2]
post.category.add(cat2)

6
post = Post.objects.all()[3]
user = User.objects.all()[0]
Comment.objects.create(post=post, user=user, text='Афтар жжот')

post = Post.objects.all()[4]
user = User.objects.all()[1]
Comment.objects.create(post=post, user=user, text='Ацтой')

post = Post.objects.all()[5]
user = User.objects.all()[0]
Comment.objects.create(post=post, user=user, text='На троечку')

post = Post.objects.all()[5]
user = User.objects.all()[1]
Comment.objects.create(post=post, user=user, text='Я твой дом труба шатал, я твой сад калитка хлопал')

7
Post.objects.all()[0].like()
Post.objects.all()[1].like()
Post.objects.all()[2].dislike()

8
from news.models import *
a = Author.objects.all()[0]
Author.update_rating(author = a)
a = Author.objects.all()[1]
Author.update_rating(author = a)

9



