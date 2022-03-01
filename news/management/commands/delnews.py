from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости в выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category = Category.objects.get(name_cat=options['category'])
            Post.objects.filter(category==category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Succesfully deleted all news from category {category.name_cat}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category}'))