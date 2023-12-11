import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import force_authenticate, APIRequestFactory
from authorz.models import F1Driver, User, Post
from authorz.views import PostList
from authorz.serializers import PostSerializer
from faker import Faker
from django.urls import reverse
client = APIClient()
fake = Faker()


@pytest.mark.django_db
def test_create_f1driver_fixture(api_client, f1driver_payload):
    url = '/api/create-f1/'
    response = api_client.post(url, f1driver_payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert F1Driver.objects.count() == 1

@pytest.mark.django_db
def test_create_f1driver():
    response = client.post('/api/create-f1/')
    assert response.status_code == 201
    f1driver = F1Driver.objects.first()
    assert f1driver is not None

def test_pytest_working():
    assert True == True

@pytest.mark.django_db
def test_create_f1driver_payload():
    client = APIClient()
    url = '/api/create-f1/'
    payload = {
        'name': 'Lewis Hamilton',
        'team': 'Mercedes',
        'country': 'England',
        'age': '38',
        'podiums': 412,
        'championships': 7,
    }
    response = client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert F1Driver.objects.count() == 1

@pytest.mark.django_db
def test_get_f1drivers(api_client, create_f1driver):
    response = api_client.get(reverse('authorz:f1driver-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    f1driver_data = dict(response.data[0]) 
    assert f1driver_data['name'] == create_f1driver.name
    assert f1driver_data['team'] == create_f1driver.team
    assert f1driver_data['country'] == create_f1driver.country
    assert f1driver_data['age'] == create_f1driver.age
    assert f1driver_data['podiums'] == create_f1driver.podiums
    assert f1driver_data['championships'] == create_f1driver.championships

@pytest.mark.django_db
def test_update_f1driver(create_f1driver):
    payload = {
        "name": fake.name(),
        "team": fake.company(),
        "country": fake.country(),
        "age": fake.random_int(min=18, max=50),
        "podiums": fake.random_int(min=0, max=100),
        "championships": fake.random_int(min=0, max=10)
    }

    # Update the record using the REST API
    client = APIClient()
    response = client.put(f'/api/f1/{create_f1driver.id}/', payload, format='json')

     # Check that the response has a 200 OK status code
    assert response.status_code == 200

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

@pytest.mark.django_db
def test_post_list_view_get_queryset():
    user = User.objects.create_user(username='testuser', email= 'test@email.com', password='testpassword')
    post = Post.objects.create(title='Test Post', body='This is a test post.', owner=user)
    factory = APIRequestFactory()
    view = PostList.as_view()
    request = factory.get('/api/posts/')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    queryset = response.data
    assert len(queryset) == 1
    assert queryset[0]['id'] == post.id

@pytest.mark.django_db
def test_post_list_view_perform_create():
    user = User.objects.create_user(username='testuser', email = 'test@email.com', password='testpassword')
    factory = APIRequestFactory()
    view = PostList.as_view()
    request = factory.post('/api/posts/', data={'title': 'Test Post', 'body': 'This is a test post.'}, format='json')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
    post = Post.objects.get(id=response.data['id'])
    assert post.owner == user