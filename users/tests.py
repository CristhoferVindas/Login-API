from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_create_user(self):
        url = '/api/create-user/'
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_create_user_invalid_password(self):
        url = '/api/create-user/'
        data = {
            'name': 'Invalid User',
            'email': 'invaliduser@example.com',
            'password': 'short',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], 'Ensure this field has at least 8 characters.')

    def test_token(self):
        url = '/api/token/'
        data = {
            'email': self.user.email,
            'password': self.user_data['password'],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_invalid_credentials(self):
        url = '/api/token/'
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_logout(self):
        url = '/api/logout/'
        refresh_token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')
        response = self.client.post(url, {'refresh': str(refresh_token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')

    def test_user_profile(self):
        url = '/api/profile/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_change_password(self):
        url = '/api/change-password/'
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': self.user_data['password'],
            'new_password': 'newpassword1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(data['new_password']))

    def test_change_password_incorrect_old(self):
        url = '/api/change-password/'
        self.client.force_authenticate(user=self.user)
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_refresh_token(self):
        url = '/api/refresh/'
        refresh_token = RefreshToken.for_user(self.user)
        response = self.client.post(url, {'refresh': str(refresh_token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
