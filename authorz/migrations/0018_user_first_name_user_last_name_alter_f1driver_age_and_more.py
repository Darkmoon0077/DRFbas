# Generated by Django 4.2.7 on 2024-01-03 15:43

from django.db import migrations, models
import faker.providers.address
import faker.providers.person


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0017_alter_f1driver_age_alter_f1driver_championships_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='age',
            field=models.PositiveIntegerField(default=35),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='championships',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='country',
            field=models.CharField(default=faker.providers.address.Provider.country, max_length=50),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='name',
            field=models.CharField(default=faker.providers.person.Provider.name, max_length=50),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='podiums',
            field=models.PositiveIntegerField(default=59),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='team',
            field=models.CharField(default='Mercedes', max_length=50),
        ),
    ]
