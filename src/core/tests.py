from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


PASSWORD = 'password'


def create_test_user() -> User:
    '''
    Returns a simple user object making an entry in database
    '''
    user = User.objects.create_user(
        username='abdullah',
        password=PASSWORD,
        first_name='Abdullah',
        last_name='Sheth',
        email='trial@demo.com'
    )
    return user


def get_access_token(username: str, password: str) -> str:
    url = reverse('login_token')
    data = {
        'username': username,
        'password': PASSWORD
    }
    client = APIClient()
    response = client.post(url, data)
    if response.status_code == 200:
        return response.data['access']


class LoginAPITests(APITestCase):

    LOGIN_URL = 'login_token'

    def setUp(self) -> None:
        self.user = create_test_user()

    def test_login_attempt(self) -> None:
        '''
        Response status is 200. Response object contains access token,
        refresh token and user object.
        '''
        url = reverse(self.LOGIN_URL)
        data = {
            'username': self.user.username,
            'password': PASSWORD
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'refresh')
        self.assertContains(response, 'access')
        self.assertContains(response, 'user')
        self.assertEquals(response.data['user']['id'], self.user.id)

    def test_invalid_password_login_attempt(self) -> None:
        '''
        For Invalid credentials, application returns 401 status code.
        '''
        url = reverse(self.LOGIN_URL)
        data = {
            'username': self.user.username,
            'password': PASSWORD + 'WRONG'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_username_login_attempt(self) -> None:
        '''
        For Invalid credentials, application returns 401 status code.
        '''
        url = reverse(self.LOGIN_URL)
        data = {
            'username': self.user.username + '123',
            'password': PASSWORD
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
