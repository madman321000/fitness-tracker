from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from .models import User


class LoginViewTests(TestCase):
    """Test cases for the login endpoint."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.login_url = reverse('accounts:login')
        
        # Create a test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            birthday=date(1990, 1, 1)
        )
    
    def test_login_with_username_success(self):
        """Test successful login with username."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIsInstance(response.data['access'], str)
        self.assertIsInstance(response.data['refresh'], str)
    
    def test_login_with_email_success(self):
        """Test successful login with email."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIsInstance(response.data['access'], str)
        self.assertIsInstance(response.data['refresh'], str)
    
    def test_login_missing_username_and_email(self):
        """Test login fails when both username and email are missing."""
        data = {
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Username or email is required')
    
    def test_login_missing_password(self):
        """Test login fails when password is missing."""
        data = {
            'username': 'testuser'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Password is required')
    
    def test_login_missing_username_email_and_password(self):
        """Test login fails when all fields are missing."""
        data = {}
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        # Should prioritize password error
        self.assertEqual(response.data['error'], 'Password is required')
    
    def test_login_wrong_password_with_username(self):
        """Test login fails with wrong password when using username."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid username/email or password')
    
    def test_login_wrong_password_with_email(self):
        """Test login fails with wrong password when using email."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid username/email or password')
    
    def test_login_invalid_username(self):
        """Test login fails with non-existent username."""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid username/email or password')
    
    def test_login_invalid_email(self):
        """Test login fails with non-existent email."""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid email or password')
    
    def test_login_disabled_user(self):
        """Test login fails for disabled user account."""
        # Disable the user
        self.test_user.is_active = False
        self.test_user.save()
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User account is disabled')
    
    def test_login_disabled_user_with_email(self):
        """Test login fails for disabled user account when using email."""
        # Disable the user
        self.test_user.is_active = False
        self.test_user.save()
        
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User account is disabled')
    
    def test_login_user_without_email(self):
        """Test login with username works for user without email."""
        # Create user without email
        user_no_email = User.objects.create_user(
            username='noemailuser',
            password='testpass123',
            birthday=date(1990, 1, 1)
        )
        
        data = {
            'username': 'noemailuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_username_takes_precedence_over_email(self):
        """Test that when both username and email are provided, username is used."""
        # Create another user with different email
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123',
            birthday=date(1990, 1, 1)
        )
        
        # Try to login with testuser's username but otheruser's email
        data = {
            'username': 'testuser',
            'email': 'other@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        
        # Should succeed because username takes precedence
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
