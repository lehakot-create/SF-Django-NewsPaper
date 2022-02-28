from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Post
from .utils import run_parser


@shared_task
def send_email(**kwargs):
    post = Post.objects.get(id=kwargs.get('pk'))
    user = User.objects.get(id=kwargs.get('user_id'))
    c = post.category.values('name_cat')[0]['name_cat']
    html_content = render_to_string(
        'news/email.html',
        {'post': post, 'user': user, 'category': c}
    )
    msg = EmailMultiAlternatives(
        subject=f'{user.username}',
        body=post.text,
        from_email='alex85aleshka@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_email_subscribers(**kwargs):
    send_mail(
        subject=f'Добавлена новость в категорию {kwargs.get("cat")}',
        message=kwargs.get('title'),
        from_email='alex85aleshka@yandex.ru',
        recipient_list=kwargs.get('email')
    )


@shared_task
def send_email_every_monday():
    all_title = Post.objects.filter(date_time__gte=datetime.now() - timedelta(days=1)).values('title')
    all_email = User.objects.values('email')
    for email in all_email:
        if email.get('email'):
            html_content = render_to_string(
                'news/mass_mailing.html',
                {'posts': all_title}
            )
            msg = EmailMultiAlternatives(
                subject=f'Новые статьи за прошедшую неделю',
                body='',
                from_email='alex85aleshka@yandex.ru',
                to=[email.get('email')],
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()


@shared_task
def run_news_parser():
    run_parser()
