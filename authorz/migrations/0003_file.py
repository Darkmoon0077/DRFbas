# Generated by Django 4.2.7 on 2023-12-04 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='files/')),
            ],
        ),
    ]
