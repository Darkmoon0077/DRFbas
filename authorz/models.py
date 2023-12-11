from datetime import datetime, timedelta
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker

fake = Faker()

class F1Driver(models.Model):
    name = models.CharField(max_length=50, default=fake.name)
    team = models.CharField(max_length=50, default=fake.random_element(elements=('Mercedes', 'Ferrari', 'Red Bull')))
    country = models.CharField(max_length=50, default=fake.country)
    age = models.PositiveIntegerField(default=fake.random_int(min=18, max=45))
    podiums = models.PositiveIntegerField(default=fake.random_int(min=0, max=100))
    championships = models.PositiveIntegerField(default=fake.random_int(min=0, max=5))

class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.uploaded_on.date()

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    def __str__(self):
        return self.email
    @property
    def token(self):
        return self._generate_jwt_token()
    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        refresh = RefreshToken.for_user(self)
        token = {
        'access': str(refresh.access_token),
        'refresh': str(refresh)}
        return token 

class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField(blank=True, default='')
    owner = models.ForeignKey('authorz.User', related_name='posts', on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        blank=True, 
        upload_to='images/thumbnails/%Y/%m/', 
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    class Meta:
        ordering = ['created']
    def __str__(self):
        return self.title

class Feedback(models.Model):
    subject = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True,)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    owner = models.ForeignKey('authorz.User', on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['-created_at']
        db_table = 'app_feedback'
    def __str__(self):
        return f'Вам письмо от {self.email}' 

class File(models.Model):
    file = models.ImageField(upload_to='files/')




