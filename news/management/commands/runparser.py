from django.core.management.base import BaseCommand, CommandError
from news.utils import run_parser


class Command(BaseCommand):
    help = 'Парсим новости'

    def handle(self, *args, **options):
        try:
            run_parser()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully parsing news'))
        except BaseException as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))