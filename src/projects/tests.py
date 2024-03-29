from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from faker import Faker
from clients.models import Client

from core.tests import PASSWORD, create_test_user, get_access_token
from clients.tests import create_test_client
from projects.models import Project, ProjectUser


faker = Faker()


def create_test_project(client: Client, user: User) -> Project:
    '''
    Returns a simple client object making an entry in database
    '''
    project = Project.objects.create(
        project_name=faker.domain_word(),
        client=client,
        created_by=user
    )
    return project


def assign_project_to_user(project: Project, user: User) -> None:
    ProjectUser.objects.create(project=project, user=user)


class ProjectAPITests(APITestCase):

    PROJECT_LIST_CREATE_API = 'project-list-create-api'

    def setUp(self) -> None:
        self.user = create_test_user()
        self.client_obj = create_test_client(self.user)
        self.project = create_test_project(self.client_obj, self.user)
        assign_project_to_user(self.project, self.user)
        access_token = get_access_token(self.user.username, PASSWORD)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_project_list_api(self) -> None:
        '''
        Response status is 200. Response object contains list of projects
        '''
        url = reverse(self.PROJECT_LIST_CREATE_API)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['project_name'],
                         self.project.project_name)

    def test_unauthenticated_project_list_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.PROJECT_LIST_CREATE_API)
        client = APIClient()
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_project_create_api(self) -> None:
        '''
        Response status is 201 if new project is successfully created.
        '''
        data = {
            'project_name': faker.domain_word(),
            'client_id': self.client_obj.id,
            'users': [self.user.id]
        }
        url = reverse(self.PROJECT_LIST_CREATE_API)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['project_name'], data['project_name'])
        self.assertEqual(
            response.data['created_by'], f'{self.user.first_name} {self.user.last_name}')
        project_user_exists = ProjectUser.objects.filter(
            project_id=response.data['id'], user=self.user).exists()
        self.assertTrue(project_user_exists)

    def test_unauthenticated_project_create_api(self) -> None:
        '''
        Response status is 401 if no authentication credentials are contained.
        '''
        url = reverse(self.PROJECT_LIST_CREATE_API)
        data = {
            'project_name': faker.domain_word(),
            'client_id': self.client_obj.id,
            'users': [self.user.id]
        }
        client = APIClient()
        response = client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_client_id_project_create_api(self) -> None:
        '''
        Response status is 400 if given client id does not exists
        '''
        data = {
            'project_name': faker.domain_word(),
            'client_id': 999999,
            'users': [self.user.id]
        }
        url = reverse(self.PROJECT_LIST_CREATE_API)
        response = self.client.post(url, data)
        error = {
            "client_id": [
                "Client with given ID does not exist."
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.data, error)
