from django.urls import path
from . import views
from .views import UserLoginView, UserLogoutView

app_name = 'authorz'
urlpatterns = [
    path('user/login/', views.LoginAPIView.as_view(), name = 'login'),
    path('user/register/', views.RegistrationAPIView.as_view(), name = 'user_register'),
    path('user/search/', views.BasicSearchAPI.as_view(), name = 'Search'),
    path('user/follow/', views.ProfileFollowAPIView.as_view(), name='profiles_messege'),
    path('user/profile/', views.ProfileListAPIView.as_view(), name='profiles_list'),
    path('user/profile/following/<int:pk>/', views.ProfileFollowingAPIView.as_view(), name='profiles_following'),
    path('user/profile/followers/<int:pk>/', views.ProfileFollowersAPIView.as_view(), name='profiles_followers'),
    path('user/profile/<int:pk>/', views.ProfileDetailAPIView.as_view(), name='profiles_detail'),
    path('user/profile/<int:pk>/update', views.ProfileUpdateAPIView.as_view(), name='profiles_update'),
    path('user/profile/<int:pk>/delete', views.ProfileDeleteAPIView.as_view(), name='profiles_delete'),
    path('login/', UserLoginView.as_view(), name='LogIn'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('reset/', views.ResetPass, name='reset'),
    path('reset/v/', views.ResetView.as_view(), name='resetV'),
    path('register', views.TestView, name= 'exp'),
    path('register/sc/', views.NewLogView.as_view(), name= 'exper'),
    path('posta/', views.PostListView.as_view(), name = 'fancy_post'),
    path('posta/create/', views.PostCreateView.as_view(), name = 'post_create'),
    path('posta/signed/', views.SignedListView.as_view(), name = 'signed_post'),
    path('users/follow/<slug:slug>/', views.ProfileFollow.as_view(), name='profile_messege'),
    path('search/', views.BasicSearch.as_view(), name = 'BaseSearch'),
    path('users/<str:slug>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('users/<str:slug>/following/', views.ProfileFollowingListView.as_view(), name='profile_following'),
    path('users/<str:slug>/followers/', views.ProfileFollowersListView.as_view(), name='profile_followers'),
    path('posta/<str:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posta/<str:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posta/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/', views.PostListAPIView.as_view(), name = 'simple_posts'),
    path('post/<int:pk>/', views.PostDetailAPIView.as_view(), name='posts_detail'),
    path('post/<int:pk>/update/', views.PostUpdateAPIView.as_view(), name='posts_update'),
    path('post/<int:pk>/delete/', views.PostDeleteAPIView.as_view(), name='posts_delete'),
    path('post/signed/', views.SignedListAPIView.as_view(), name = 'signed_posts'),
    
]