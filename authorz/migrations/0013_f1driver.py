# Generated by Django 4.2.7 on 2023-12-11 10:45

from django.db import migrations, models
import faker.providers.address
import faker.providers.person


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0012_alter_feedback_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='F1Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=faker.providers.person.Provider.name, max_length=50)),
                ('team', models.CharField(default='Ferrari', max_length=50)),
                ('country', models.CharField(default=faker.providers.address.Provider.country, max_length=50)),
                ('age', models.PositiveIntegerField(default=24)),
                ('podiums', models.PositiveIntegerField(default=95)),
                ('championships', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
