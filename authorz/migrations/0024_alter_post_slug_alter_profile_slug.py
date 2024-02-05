# Generated by Django 4.2.7 on 2024-01-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0023_alter_post_slug_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=16, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=16, unique=True, verbose_name='URL'),
        ),
    ]