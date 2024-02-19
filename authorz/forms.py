import random, string
from .models import Profile, User, Post, ChatMessage
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')
        widgets = {
                'birth_date' : DateInput(),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['bio'].widget.attrs['placeholder'] = 'Краткая информация о себе'
            self.fields['birth_date'].label = 'Date of birth'
            self.fields['bio'].label = 'Profile bio'
            self.fields['avatar'].label = "Выберите изображение с допустимым форматом (png, jpg, jpeg)"
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Логин пользователя', 'class': 'form-control', 'autocomplete': 'off'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email пользователя', 'class': 'form-control', 'autocomplete': 'off', 'readonly': True}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'form-control', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия пользователя', 'class': 'form-control', 'autocomplete': 'off'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        u = User.objects.filter(username=username).first()
        if u is None:
            u = User.objects.filter(email=email).first()
        id = u.id
        if email and User.objects.filter(email=email).exclude(pk=id).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name.isalpha():
            raise forms.ValidationError('Имя должно содержать только буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.isalpha():
            raise forms.ValidationError('Фамилия должна содержать только буквы')
        return last_name
    

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Email пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['username'].label = 'Email'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'sdescription', 'body', 'thumbnail')
    def make_slug(self):
        while True:
            random_slug = ''.join(random.choices(string.digits, k=8))
            if not Post.objects.filter(slug=random_slug).exists():
                break 
        return random_slug
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['title'].widget.attrs['placeholder'] = 'Заголовок статьи'
            self.fields['title'].label = 'Post title'
            self.fields['sdescription'].widget.attrs['placeholder'] = 'Короткая аннотация статьи'
            self.fields['sdescription'].label = 'Post short descriptions'
            self.fields['body'].widget.attrs['placeholder'] = 'Содержание статьи'
            self.fields['body'].label = 'Post body'
            self.fields['thumbnail'].label = "Выберите изображение с допустимым форматом (png, jpg, webp, jpeg, gif)"
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['slug'] = forms.SlugField(widget=forms.HiddenInput(), required=False)
    def clean_slug(self):
        if not self.cleaned_data['slug']:
            return self.make_slug()
        return self.cleaned_data['slug']
    


class PostUpdateForm(PostCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RegForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LogForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PassForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    npassword = forms.CharField(label='New Password', required=True, widget=forms.PasswordInput)
    rpassword = forms.CharField(label='Repeat the Password', required=True, widget=forms.PasswordInput)

class SearchForm(forms.Form):
    que = forms.CharField()

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']