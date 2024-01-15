import pytest
import ast
from rest_framework import status
from rest_framework.test import APIClient
from authorz.models import User, Post, Profile
from django.urls import reverse

@pytest.mark.django_db
def test_create_user_payload():
    client = APIClient()
    url = '/api/user/register/'
    payload = {
        'user': {
            'email': 'mercedes@gmail.com',
            'username': 'LewisHamilton',
            'password': 'Mercedes1'}
    }
    response = client.post(url, payload, format = 'json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_login_user_payload():
    client = APIClient()
    client.post('/api/user/register/',data={'user': {
            'email': 'mercedes@gmail.com',
            'username': 'LewisHamilton',
            'password': 'Mercedes1'}
    }, format = 'json')
    url = reverse('authorz:login')
    payload = {
        'user': {
            'email': 'mercedes@gmail.com',
            'password': 'Mercedes1'}
    }
    response = client.post(url, data=payload, format = 'json')
    print(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data

@pytest.mark.django_db
def test_post_list_unauthenticated():
    client = APIClient()
    url = reverse('authorz:simple_posts') 
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_post_detail_api_view_authenticated_user(client):
    client = APIClient()
    response = client.post('/api/user/register/', data={'user': {'email': 'mercedes@gmail.com', 'username': 'LewisHamilton', 'password': 'Mercedes1'}}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(email='mercedes@gmail.com')
    client.force_authenticate(user=user)
    post = Post.objects.create(title='Test Post', body='This is a test post', slug = 'EWR', owner=user)
    response = client.get(f'/api/post/{post.id}/')
    assert response.status_code == status.HTTP_200_OK
    response = client.patch(f'/api/post/{post.id}/update/', title = 'Est POst')
    assert response.status_code == status.HTTP_200_OK
    response = client.delete(f'/api/post/{post.id}/delete/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
@pytest.mark.django_db
def test_profile_follow_api_view():
    user1 = User.objects.create_user(email = 'user1@gmail.com', username='user1', password='password1')
    user2 = User.objects.create_user(email = 'user2@gmail.com', username='user2', password='password2')
    client = APIClient()
    response = client.post('/api/user/login/', {'user': {'email': 'user1@gmail.com', 'password': 'password1'}}, format='json')
    assert response.status_code == 200
    token_str = response.data['token']
    token_dict = ast.literal_eval(token_str)
    access_token = token_dict['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.post(f'/api/user/follow/{user2.id}/')
    assert response.status_code == 200
    assert response.data == "You subscribed"
    response = client.get(f'/api/user/profile/followers/{user2.id}/')
    assert response.status_code == 200
    response = client.get(f'/api/user/profile/following/{user1.id}/')
    assert response.status_code == 200
    response = client.post(f'/api/user/follow/{user2.id}/')
    assert response.status_code == 200
    assert response.data == "You unsubscribed"