# Generated by Django 4.0 on 2021-12-11 20:00

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_newuser_alter_comment_post_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, verbose_name=django.contrib.auth.models.User)),
            ],
        ),
        migrations.DeleteModel(
            name='NewUser',
        ),
    ]
