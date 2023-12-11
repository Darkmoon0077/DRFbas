import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from authorz.models import F1Driver, Post, User
from authorz.serializers import PostSerializer
from rest_framework.test import APIClient
@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def f1driver_payload():
    payload = {
        'name': 'Lewis Hamilton',
        'team': 'Mercedes',
        'country': 'England',
        'age': 38,
        'podiums': 412,
        'championships': 7,
    }
    return payload

@pytest.fixture
def create_f1driver():
    payload = {
        'name': 'Lewis Hamilton',
        'team': 'Mercedes',
        'country': 'England',
        'age': 38,
        'podiums': 412,
        'championships': 7,
    }
    record =F1Driver.objects.create(**payload)
    return record

@pytest.fixture
def create_Post_user():
    payload = {
        'user': {
            'email': 'mercedes@gmail.com',
            'username': 'LewisHamilton',
            'password': 'Mercedes'}
    }
    record =Post.objects.create(**payload)
    return record

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email= 'test@email.com', password='testpassword')

@pytest.fixture
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)

@pytest.fixture
def authenticated_client(refresh_token, client):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token}')
    return client


