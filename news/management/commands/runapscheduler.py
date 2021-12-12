import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from ...models import CategorySubscribers, Post, Category
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from ...utils import run_parser

logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...
    print('hello from job')
    all = CategorySubscribers.objects.values()
    for el in all:
        cat_id = el['category_id']
        subscriber = User.objects.get(id=el['subscribers_id']).email
        try:
            all_news = Post.objects.filter(category=cat_id, date_time__gte=datetime.today() - timedelta(7)).values('title')[0]['title']
            send_mail(
                subject='Свежие новости за последнюю неделю',
                message=f'Новости из категории {Category.objects.get(id=cat_id).name_cat}\n'
                        f'{all_news}',
                from_email='alex85aleshka@yandex.ru',
                recipient_list=[subscriber]
            )
        except IndexError:
            pass
    print('job is done')


def job_parser():
    #  Your job processing logic here...
    print('hello from job_parser')
    run_parser()
    print('job_parser is done')


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            job_parser,
            trigger=CronTrigger(hour="12"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="job_parser",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'job_parser'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")