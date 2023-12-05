from django.urls import path
from . import views


app_name = 'authorz'
urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('file/upload/', views.FileUploadView.as_view(), name='file-upload'),
]