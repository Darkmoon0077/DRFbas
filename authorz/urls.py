from django.urls import path
from . import views
from . import tasks

app_name = 'authorz'
urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('post/', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('file/upload/', tasks.FileUploadView.as_view(), name='file-upload'),
    path('upload-file/', views.FileUploadAPIView.as_view(), name='upload-file'), 
    path('feedback/', views.FeedbackCreateView.as_view(), name='feedback'),
    path('contact/', views.contact_view, name='contact'),
    path('success/', views.success_view, name='success'),
    path('ind/', views.index),
    path('send-mail/', views.send_mail_view),
    path('send/', views.skend),
]