from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .services.utils import unique_slugify

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
    first_name = models.CharField( max_length=30, blank=True)
    last_name = models.CharField( max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_password_update = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    def __str__(self):
        return self.email
    def update_password(self, new_password):
        self.password = make_password(new_password)
        self.last_password_update = timezone.now()
        self.save()
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
    slug = models.SlugField(verbose_name='URL', max_length=16, blank=False, unique=True)
    thumbnail = models.ImageField(
        blank=True, 
        upload_to='images/thumbnails/%Y/%m/', 
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    class Meta:
        ordering = ['created']
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('authorz:post_detail', kwargs={'slug': self.slug}) 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=16, blank=False, unique=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/', 
        default='images/avatars/default.jpg',
        blank=True,  
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = 'app_profiles'
        ordering = ('user',)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('authorz:profile_detail', kwargs={'slug': self.slug})
    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


