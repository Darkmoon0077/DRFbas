# Generated by Django 4.2.7 on 2024-02-15 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0028_post_sdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=24, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=24, unique=True, verbose_name='URL'),
        ),
    ]
