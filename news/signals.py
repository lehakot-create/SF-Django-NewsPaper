from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Post, CategorySubscribers, Category
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.category.through)
def send_message(sender, instance, action, **kwargs):
    if action == 'post_add':
        id = instance.category.values('id')[0]['id']
        cat = Category.objects.get(id=id)
        lst = cat.subscribers.all()
        email = []
        for el in lst:
            email.append(el.email)

        send_mail(
            subject=f'Добавлена новость в категорию {cat}',
            message=instance.title,
            from_email='alex85aleshka@yandex.ru',
            recipient_list=email
        )

