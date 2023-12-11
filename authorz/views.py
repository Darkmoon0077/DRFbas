from rest_framework import status, generics, permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from . import serializers
from .forms import FeedbackCreateForm, ContactForm
from .models import Post, Feedback
from .permissions import IsOwnerOrReadOnly
from .renderers import UserJSONRenderer
from .serializers import RegistrationSerializer, LoginSerializer, PostSerializer
from .serializers import UploadSerializer
from .services.email import send_contact_email_message
from .services.utils import get_client_ip
from .tasks import keksend, brend
from django.conf.global_settings import EMAIL_HOST_USER
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError

@csrf_exempt
def skend(request):
    if request.method == 'POST':
        brend.delay() 
        return HttpResponse('Email sending task started successfully!')
    else:
        return HttpResponse('Invalid request method')

@csrf_exempt
def send_mail_view(request):
    if request.method == 'POST':
        try:
            send_mail('JJJ', 'kkk', 'darkmoon0077@gmail.com', ['Darkmoon077@yandex.kz', 'aidaraimbekova99@gmail.com'], fail_silently=False)
            return HttpResponse('Email sent successfully!')
        except Exception as e:  
            return HttpResponse('Email wasnt sent successfully!')
    else: return HttpResponse('Email wasnt sent successfully!')

def index(request):
    return render(request, 'index.html')

def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Assuming you only pass the relevant form data to the task
            keksend.delay(form.cleaned_data)
            return HttpResponse("Task started successfully.")
        else:
            return HttpResponse("Form is not valid.")
    else:
        return HttpResponse('Неверный запрос.')

def success_view(request):
    return HttpResponse('Приняли! Спасибо за вашу заявку.')

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
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        user = request.data.get('user', {})
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