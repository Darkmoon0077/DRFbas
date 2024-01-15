from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, DeleteView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from . import serializers, forms
from .forms import LogForm, PassForm, ProfileUpdateForm, UserUpdateForm, UserLoginForm
from .models import Post, User, Profile
from .permissions import IsOwnerOrReadOnly
from .renderers import UserJSONRenderer
from .serializers import RegistrationSerializer, LoginSerializer, PostSerializer



class ProfileFollow(LoginRequiredMixin, View):
    model = Profile
    renderer_classes = (UserJSONRenderer,)
    @swagger_auto_schema(
        operation_summary="Follow or unfollow a user profile",
        manual_parameters=[
            openapi.Parameter(
                'slug',
                openapi.IN_PATH,
                description="User profile slug",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={302: "Redirect to profile detail page"},
    )
    def post(self, request, slug,  *args, **kwargs):
        if not slug:
            return Response({'error': 'Slug is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        print(profile)
        print(request.user.profile.following.all())
        if profile in request.user.profile.following.all():
            request.user.profile.following.remove(profile)
        elif profile not in request.user.profile.following.all():
            request.user.profile.following.add(profile)
        return redirect('authorz:profile_detail', slug=slug)

class BasicSearch(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        form = forms.SearchForm()
        return render(request, 'index.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = forms.SearchForm(request.POST)
        print(request.POST)
        if form.is_valid():
            query = form.cleaned_data['que']
            poofs = User.objects.filter(Q(username__icontains = query) | Q(email__icontains = query))
            if poofs.exists():
                for user_object in poofs:
                    user_id = user_object.id
                    profile = Profile.objects.get(user=user_object)
                    print(f"Profile associated with user {user_id}: {profile}")
                    mata = profile.slug
                    return redirect(f'/api/users/{mata}/')
            else:
                return redirect(reverse('authorz:BaseSearch'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Search'
        return context        

class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'authorz/profile_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context

class ProfileFollowingListView(DetailView):
    template_name = 'authorz/profile_list.html'
    def post(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        followers = profile.following.all
        return render(request, self.template_name, {'profile': profile, 'followers': followers})

class ProfileFollowersListView(DetailView):
    template_name = 'authorz/profile_list.html'
    def post(self, request, slug):
        profile = get_object_or_404(Profile, slug=slug)
        followers = profile.followers.all
        return render(request, self.template_name, {'profile': profile, 'followers': followers})

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
    return render(request, 'authorz/user_register.html')
class NewLogView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        form = forms.RegForm()
        return render(request, 'authorz/user_register.html', {'form': form})
    @swagger_auto_schema(auto_schema=None)
    def post(self, request, *args, **kwargs):
        form = forms.RegForm(request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = {
                    "email": email,
                    "username": username,
                    "password": password
                }
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        form = LogForm()
        return render(request, 'authorz/reset.html', {'form': form})
    @swagger_auto_schema(auto_schema=None)
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

class UserLoginView(LoginView):
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

class SignedListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'list.html'
    context_object_name = 'posts'
    authentication_classes = (JWTAuthentication)
    login_url = 'login'
    def get_queryset(self):
        authors = self.request.user.profile.following.values_list('id', flat=True)
        print(authors)
        linked = User.objects.filter(profile__id__in=authors).values_list('id', flat=True)
        print(linked)
        queryset = self.model.objects.all().filter(owner_id__in=linked)
        print(queryset)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List' 
        return context

class PostListView(ListView):
    model = Post
    permission_classes = (AllowAny,)
    template_name = 'list.html'
    context_object_name = 'posts'
    @swagger_auto_schema(
        operation_summary="Get a list of posts",
        responses={200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))},)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Post List' 
        return context

class PostCreateView(CreateView):
    model = Post
    template_name = 'authorz/post_create.html'
    form_class = forms.PostCreateForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context
    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)
    
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'authorz/post_update.html'
    context_object_name = 'posts'
    form_class = forms.PostUpdateForm
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('authorz:fancy_post')
    context_object_name = 'post'
    template_name = 'authorz/post_delete.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'authorz/post_detail.html'
    context_object_name = 'Post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    @swagger_auto_schema(
    operation_summary="Submit reset form",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=['email', 'password'],
            ),
        },
        required=['user'],
    ),
    responses={200: RegistrationSerializer()},
    )
    def post(self, request):
        user = request.data.get('user', {})
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    @swagger_auto_schema(
    operation_summary="Submit reset form",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING),
                    
                },
                required=['email', 'username', 'password'],
            ),
        },
        required=['user'],
    ),
    responses={201: RegistrationSerializer()},
    )
    def post(self, request):
        user = request.data.get('user', {})
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProfileDeleteAPIView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
class ProfileFollowingAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk,  *args, **kwargs):
        profiles = User.objects.get(id=pk)
        profile1 = profiles.id
        profile = Profile.objects.get(user=profile1)
        following_objects = profile.following.all()
        u1 = profile.user.username
        serializer = serializers.ProfileSerializer(following_objects, many=True)
        data = {
            "Профиль": u1,
            "Подписки": serializer.data
        }
        return Response(data)

class ProfileFollowersAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk,  *args, **kwargs):
        profiles = User.objects.get(id=pk)
        profile1 = profiles.id
        profile = Profile.objects.get(user=profile1)
        following_objects = profile.followers.all()
        u1 = profile.user.username
        serializer = serializers.ProfileSerializer(following_objects, many=True)
        data = {
            "Профиль": u1,
            "Подписчики": serializer.data
        }
        return Response(data)

class PostListAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_queryset(self):
        return Post.objects.all()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class BasicSearchAPI(APIView):
    serializer_class = serializers.SearchSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Submit search form",
        manual_parameters=[
            openapi.Parameter(
                name='query',
                in_=openapi.IN_QUERY,
                description='Search query for username or email.',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: serializers.SearchSerializer()},
    )
    def get(self, request, *args, **kwargs):
        query = self.request.query_params.get('query')
        print(query)
        if not query:
            return Response({"error": "Invalid query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        poofs = User.objects.filter(Q(username__icontains = query) | Q(email__icontains = query))
        serializer = serializers.SearchSerializer(poofs, many=True)
        data = {
            "Keyword": query,
            "Results": serializer.data
        }
        return Response(data)

class ProfileFollowAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk,  *args, **kwargs):
        try:
            profiles = Profile.objects.filter(user_id=pk)
            profile = profiles.first()
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        if profile in request.user.profile.following.all():
            request.user.profile.following.remove(profile)
            return Response("You unsubscribed")
        elif profile not in request.user.profile.following.all():
            request.user.profile.following.add(profile)
            return Response("You subscribed")

class SignedListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    model = Post
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        current_user = self.request.user
        if hasattr(current_user, 'profile'):
            authors = current_user.profile.following.values_list('id', flat=True)
            linked = User.objects.filter(profile__id__in=authors).values_list('id', flat=True)
            return Post.objects.filter(owner_id__in=linked)
        return Post.objects.none()


