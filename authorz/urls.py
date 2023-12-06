from django.urls import path, include
from . import views
from . import tasks
from rest_framework.routers import DefaultRouter
from .views import ImgViewSet
router = DefaultRouter()
router.register(r'Img', ImgViewSet, basename='Img')

app_name = 'authorz'
urlpatterns = [
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('file/upload/', tasks.FileUploadView.as_view(), name='file-upload'),
    path('upload-file/', views.FileUploadAPIView.as_view(), name='upload-file'), 
    path('', include(router.urls)),
    path('api/Img/<int:pk>/', views.ImageRetrieveView.as_view(), name='image-retrieve'),
]