# Generated by Django 4.2.7 on 2024-01-03 12:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import faker.providers.address
import faker.providers.person


class Migration(migrations.Migration):

    dependencies = [
        ('authorz', '0014_user_last_password_update_alter_f1driver_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='f1driver',
            name='age',
            field=models.PositiveIntegerField(default=44),
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
            field=models.PositiveIntegerField(default=54),
        ),
        migrations.AlterField(
            model_name='f1driver',
            name='team',
            field=models.CharField(default='Red Bull', max_length=50),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL')),
                ('avatar', models.ImageField(blank=True, default='images/avatars/default.jpg', upload_to='images/avatars/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Аватар')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='authorz.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'app_profiles',
                'ordering': ('user',),
            },
        ),
    ]
