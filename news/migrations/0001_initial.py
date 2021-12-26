# Generated by Django 4.0 on 2021-12-26 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(default=0, verbose_name='Рейтинг')),
                ('full_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cat', models.CharField(max_length=62, unique=True, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.CharField(choices=[('Article', 'Статья'), ('News', 'Новость')], default='Article', max_length=7, verbose_name='Тип')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Заголовок')),
                ('text', models.TextField(max_length=255, verbose_name='Текст новости')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('url', models.URLField(verbose_name='Адрес')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категория')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Пост')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.Category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Статья')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
