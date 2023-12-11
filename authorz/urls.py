from django.urls import path
from . import views
from . import tasks

app_name = 'authorz'
urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view(), name = 'login'),
    path('posts/', views.PostList.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('post/', views.PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('file/upload/', tasks.FileUploadView.as_view(), name='file-upload'),
    path('upload-file/', views.FileUploadAPIView.as_view(), name='upload-file'), 
    path('feedback/', views.FeedbackCreateView.as_view(), name='feedback'),
    path('ind/', views.index),
    path('send/', views.skend),
    path('create-f1/', views.F1DriverCreateView.as_view(), name='create-f1driver'),
    path('f1/', views.F1DriverList.as_view(), name='f1driver-list'),
    path('f1/<int:pk>/', views.F1DriverUpdateView.as_view(), name='f1driver_update'),
]