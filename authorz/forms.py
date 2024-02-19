from .models import Profile, User, Post, ChatMessage
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['bio'].widget.attrs['placeholder'] = 'Краткая информация о себе'
            self.fields['birth_date'].widget.attrs['placeholder'] = 'Укажите дату рождения в формате YYYY-DD-MM'
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['email'].widget.attrs['placeholder'] = 'Email пользователя'
            self.fields['first_name'].widget.attrs['placeholder'] = 'Имя пользователя'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия пользователя'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
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
        fields = ('title', 'sdescription', 'body', 'thumbnail')
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