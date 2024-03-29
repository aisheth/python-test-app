from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from faker import Faker

from core.tests import PASSWORD, create_test_user, get_access_token
from clients.models import Client


faker = Faker()

def create_test_client(user) -> Client:
    '''
    Returns a simple client object making an entry in database
    '''
    client = Client.objects.create(
        client_name = faker.company(),
        created_by = user
    )
    return client


class ClientAPITests(APITestCase):

    CLIENT_LIST_CREATE_API = 'client-list-create-api'
    CLIENT_RETRIEVE_UPDATE_API = 'client-retrieve-update-api'

    def setUp(self) -> None:
        self.user = create_test_user()  
        self.client_obj = create_test_client(self.user)
        access_token = get_access_token(self.user.username, PASSWORD)
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {access_token}')

    def test_client_list_api(self) -> None:
        '''
        Response status is 200. Response object contains list of clients
        '''
        url = reverse(self.CLIENT_LIST_CREATE_API)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_client_list_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.CLIENT_LIST_CREATE_API)
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_create_api(self) -> None:
        '''
        Response status is 201 if new client details are created.
        '''
        data = {
            'client_name': 'Client B'
        }
        url = reverse(self.CLIENT_LIST_CREATE_API)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['client_name'], data['client_name'])
        self.assertEqual(response.data['created_by'], self.user.username)

    def test_unauthenticated_client_create_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.CLIENT_LIST_CREATE_API)
        data = {
            'client_name': 'Client B'
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_update_api(self) -> None:
        '''
        Response status is 200 if client details are updated.
        '''
        data = {
            'client_name': 'Client C'
        }
        url = reverse(self.CLIENT_RETRIEVE_UPDATE_API, 
                        kwargs={'pk': self.client_obj.id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['client_name'], data['client_name'])

    def test_unauthenticated_client_update_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.CLIENT_RETRIEVE_UPDATE_API, 
                        kwargs={'pk': self.client_obj.id})
        data = {
            'client_name': 'Client C'
        }
        client = APIClient()
        response = client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_delete_api(self) -> None:
        '''
        Response status is 204 if client details is deleted.
        '''
        client_obj = Client.objects.create(client_name='Client D',
                                            created_by=self.user)
        url = reverse(self.CLIENT_RETRIEVE_UPDATE_API, 
                        kwargs={'pk': client_obj.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        client_exists = Client.objects.filter(id=client_obj.id).exists()
        self.assertFalse(client_exists)

    def test_unauthenticated_client_delete_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.CLIENT_RETRIEVE_UPDATE_API, 
                        kwargs={'pk': self.client_obj.id})

        client = APIClient()
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
