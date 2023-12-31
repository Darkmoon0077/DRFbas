# Generated by Django 4.2.7 on 2024-01-03 17:31

from django.db import migrations, models
import faker.providers.address
import faker.providers.person


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0018_user_first_name_user_last_name_alter_f1driver_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='f1driver',
            name='age',
            field=models.PositiveIntegerField(default=21),
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
            field=models.PositiveIntegerField(default=51),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='team',
            field=models.CharField(default='Ferrari', max_length=50),
        ),
    ]
