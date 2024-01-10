import pytest
from rest_framework import status
from rest_framework.test import APIClient
from authorz.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_create_user_payload():
    client = APIClient()
    url = '/api/users/'
    payload = {
        'user': {
            'email': 'mercedes@gmail.com',
            'username': 'LewisHamilton',
            'password': 'Mercedes'}
    }
    response = client.post(url, payload, format = 'json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_login_user_payload():
    client = APIClient()
    client.post('/api/users/',data={'user': {
            'email': 'mercedes@gmail.com',
            'username': 'LewisHamilton',
            'password': 'Mercedes'}
    }, format = 'json')
    url = reverse('authorz:login')
    payload = {
        'user': {
            'email': 'mercedes@gmail.com',
            'password': 'Mercedes'}
    }
    response = client.post(url, data=payload, format = 'json')
    print(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data

@pytest.mark.django_db
def test_post_list_unauthenticated():
    client = APIClient()
    url = reverse('authorz:posts') 
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


