from django.urls import path
from . import views
from . import tasks
from .views import ProfileUpdateView, ProfileDetailView, UserRegisterView, UserLoginView, UserLogoutView

app_name = 'authorz'
urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='LogIn'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/', views.RegistrationAPIView.as_view()),
    path('users/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('users/login/', views.LoginAPIView.as_view(), name = 'login'),
    path('reset/', views.ResetPass, name='reset'),
    path('reset/v/', views.ResetView.as_view(), name='resetV'),
    path('a/', views.TestView, name= 'exp'),
    path('a/login/', views.NewLogView.as_view(), name= 'exper'),
    path('posts/', views.PostList.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('post/', views.PostListView.as_view(), name='home'),
    path('posta/', views.AListView.as_view(), name = 'fancy_post'),
    path('posta/create/', views.PostCreateView.as_view(), name = 'post_create'),
    path('file/upload/', tasks.FileUploadView.as_view(), name='file-upload'),
    path('upload-file/', views.FileUploadAPIView.as_view(), name='upload-file'), 
    path('feedback/', views.FeedbackCreateView.as_view(), name='feedback'),
    path('ind/', views.Loggedin.as_view(), name = 'welcome'),
    path('send/', views.skend), 
    path('users/follow/<slug:slug>/', views.ProfileFollow.as_view(), name='profile_messege'),
    path('search/', views.BasicSearch.as_view(), name = 'BaseSearch'),
    path('users/<str:slug>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('users/<str:slug>/following/', views.ProfileFollowingListView.as_view(), name='profile_following'),
    path('users/<str:slug>/followers/', views.ProfileFollowersListView.as_view(), name='profile_followers'),
    path('posta/<str:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posta/<str:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posta/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]