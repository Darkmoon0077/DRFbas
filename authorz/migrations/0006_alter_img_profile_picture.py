# Generated by Django 4.2.7 on 2023-12-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0005_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='profile_picture',
            field=models.BinaryField(),
        ),
    ]
