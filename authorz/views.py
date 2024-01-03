from rest_framework import status, generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView


from . import serializers
from .forms import FeedbackCreateForm, LogForm, PassForm, ProfileUpdateForm, UserUpdateForm, UserRegisterForm, UserLoginForm
from .models import Post, Feedback, F1Driver, User, Profile
from .permissions import IsOwnerOrReadOnly
from .renderers import UserJSONRenderer
from .serializers import RegistrationSerializer, LoginSerializer, PostSerializer, F1DriverSerializer
from .serializers import UploadSerializer
from .services.email import send_contact_email_message
from .services.utils import get_client_ip
from .tasks import brend
from django.views.decorators.csrf import csrf_exempt


@method_decorator(login_required, name='dispatch')
class ProfileFollowingCreateView(View):
    model = Profile
    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    def post(self, request, slug):
        user = self.model.objects.get(slug=slug)
        profile = request.user.profile
        if profile in user.followers.all():
            user.followers.remove(profile)
            message = f'Подписаться на {user}'
            status = False
        else:
            user.followers.add(profile)
            message = f'Отписаться от {user}'
            status = True
        data = {
            'username': profile.user.username,
            'get_absolute_url': profile.get_absolute_url(),
            'slug': profile.slug,
            'avatar': profile.get_avatar,
            'message': message,
            'status': status,
        }
        return JsonResponse(data, status=200)

class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'authorz/profile_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'authorz/profile_edit.html'
    def get_object(self, queryset=None):
        return self.request.user.profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('authorz:profile_detail', kwargs={'slug': self.object.slug})

def TestView(request):
    return render(request, 'authorz/login.html')
class NewLogView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    def get(self, request, *args, **kwargs):
        form = LogForm()
        return render(request, 'authorz/login.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = LogForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = {
                    "email": email,
                    "password": password
                }
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            if self.password_check(email):
                return redirect(reverse('authorz:reset'))
            return Response(serializer.data, status=status.HTTP_200_OK)
    def password_check(self, email):
        try:
            user = User.objects.get(email=email)
            if user.last_password_update:
                time_difference = timezone.now() - user.last_password_update
                return time_difference > timedelta(days=20)
            return False
        except User.DoesNotExist:
            return False


def ResetPass(request):
    return render(request, 'authorz/reset.html')
class ResetView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    def get(self, request, *args, **kwargs):
        form = LogForm()
        return render(request, 'authorz/reset.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = PassForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            npassword = form.cleaned_data['npassword']
            rpassword = form.cleaned_data['rpassword']
            user = {
                    "email": email,
                    "password": password
                }
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            if npassword != rpassword:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            user.update_password(npassword)
            user = {
                    "email": email,
                    "password": npassword
                }
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

class CustomLoginView(LoginView):
    template_name = 'authorz/login.html'
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('authorz:fancy_post')
    template_name = 'authorz/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'authorz/user_login.html'
    next_page = 'authorz:fancy_post'
    success_message = 'Добро пожаловать на сайт!'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context

class UserLogoutView(LogoutView):
    next_page = 'authorz:fancy_post'

class F1DriverCreateView(APIView):
    """create view"""
    def post(self, request):
        f1driver = F1Driver.objects.create()
        serializer = F1DriverSerializer(f1driver)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class F1DriverList(generics.ListAPIView):
    """get view"""
    queryset = F1Driver.objects.all()
    serializer_class = F1DriverSerializer

class F1DriverUpdateView(generics.UpdateAPIView):
    """update view"""
    queryset = F1Driver.objects.all()
    serializer_class = F1DriverSerializer

@csrf_exempt
def skend(request):
    if request.method == 'POST':
        brend.delay() 
        return HttpResponse('Email sending task started successfully!')
    else:
        return HttpResponse('Invalid request method')

class Loggedin(LoginView):
    template_name = 'index.html'

class AListView(ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List' 
        return context

class PostListView(ListView):
    model = Post
    template_name = 'authorz/post_list.html'
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List'
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'authorz/post_detail.html'
    context_object_name = 'Post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED  )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        user = request.data.get('user', {})
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class FeedbackCreateView(APIView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    extra_context = {'title': 'Контактная форма'}
    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address, feedback.user_id)
        return super().form_valid(form)