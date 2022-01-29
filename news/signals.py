from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from .tasks import send_email_subscribers


@receiver(m2m_changed, sender=Post.category.through)
def send_message(sender, instance, action, **kwargs):
    if action == 'post_add':
        id = instance.category.values('id')[0]['id']
        cat = Category.objects.get(id=id)
        lst = cat.subscribers.all()
        email = []
        for el in lst:
            email.append(el.email)

        send_email_subscribers.apply_async(kwargs={'cat': cat.name_cat,
                                                   'title': instance.title,
                                                   'email': email,
                                                   }
                                           )
