python manage.py shell
from news.models import *


1
User.objects.create_user('bob')
User.objects.create_user('jack')
User.objects.create_user('jully')
User.objects.create_user('jenny')

2
Author.objects.create(full_name=User.objects.all()[0])
Author.objects.create(full_name=User.objects.all()[1])
Author.objects.create(full_name=User.objects.get(id=18))

3

Category.objects.create(name_cat='45.ru')
Category.objects.create(name_cat='74.ru')
Category.objects.create(name_cat='angi.ru')
Category.objects.create(name_cat='neftegaz.ru')
Category.objects.create(name_cat='ria.ru')
Category.objects.create(name_cat='ria56')
Category.objects.create(name_cat='sarnovosti.ru')
Category.objects.create(name_cat='Tatar_inform')
Category.objects.create(name_cat='ufa1')

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
post = Post.objects.all()[0]
user = User.objects.all()[0]
Comment.objects.create(post=post, user=user, text='Афтар жжот')

post = Post.objects.all()[1]
user = User.objects.all()[1]
Comment.objects.create(post=post, user=user, text='Ацтой')

post = Post.objects.all()[1]
user = User.objects.all()[0]
Comment.objects.create(post=post, user=user, text='На троечку')

post = Post.objects.all()[2]
user = User.objects.all()[1]
Comment.objects.create(post=post, user=user, text='Я твой дом труба шатал, я твой сад калитка хлопал')

7
Post.objects.all()[0].like()
Post.objects.all()[1].like()
Post.objects.all()[2].dislike()

8
a = Author.objects.all()[0]
Author.update_rating(author = a)
a = Author.objects.all()[1]
Author.update_rating(author = a)

9
a = Author.objects.order_by('-rating').first().full_name_id
User.objects.filter(id = a).values('username')[0]['username']

10
p = Post.objects.order_by('-rating').first()
p.date_time
User.objects.filter(id = p.author_id).values('username')[0]['username']
p.rating
p.title
p.preview()

11
p_id = Post.objects.order_by('-rating').first().id
Comment.objects.filter(post_id = p_id).values('date_time')
Comment.objects.filter(post_id = p_id).values('user_id')
Comment.objects.filter(post_id = p_id).values('rating')
Comment.objects.filter(post_id = p_id).values('text')




post = Post.objects.create(author=Author.objects.get(id=2), choices='News',title='GПрограмма максимум:  показать все что скрыто', text='GВнимание! Внимание! Сегодня под мостом нашли Гитлера с хвостом', url='http://')


Post.objects.get(id=1)