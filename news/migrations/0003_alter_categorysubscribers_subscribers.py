# Generated by Django 4.0 on 2022-01-14 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0002_categorysubscribers_category_subscribers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorysubscribers',
            name='subscribers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]