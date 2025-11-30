from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from accounts.models import User
from .models import Exercise


class ExerciseViewTests(TestCase):
    """Test cases for the exercise endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.create_url = reverse('exercises:create_exercise')
        self.get_url = reverse('exercises:get_exercises')
        
        # Create test users
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            birthday=date(1990, 1, 1)
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123',
            birthday=date(1990, 1, 1)
        )
        
        # Get JWT token for test_user
        refresh = RefreshToken.for_user(self.test_user)
        self.access_token = str(refresh.access_token)
    
    def _authenticate(self, user=None):
        """Helper method to authenticate the client."""
        if user is None:
            user = self.test_user
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def _unauthenticate(self):
        """Helper method to remove authentication."""
        self.client.credentials()
    
    # CREATE EXERCISE TESTS
    
    def test_create_reps_weight_exercise_success(self):
        """Test successful creation of reps+weight exercise."""
        self._authenticate()
        data = {
            'exercise_type': 'reps_weight',
            'description': 'Bench press with proper form',
            'weight': 100.5,
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['exercise_type'], 'reps_weight')
        self.assertEqual(response.data['description'], 'Bench press with proper form')
        self.assertEqual(float(response.data['weight']), 100.5)
        self.assertEqual(response.data['reps'], 10)
        self.assertIsNone(response.data['time_seconds'])
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        
        # Verify exercise was saved to database
        exercise = Exercise.objects.get(id=response.data['id'])
        self.assertEqual(exercise.user, self.test_user)
        self.assertEqual(exercise.exercise_type, 'reps_weight')
    
    def test_create_time_weight_exercise_success(self):
        """Test successful creation of time+weight exercise."""
        self._authenticate()
        data = {
            'exercise_type': 'time_weight',
            'description': 'Plank hold',
            'weight': -20.0,
            'time_seconds': 60
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['exercise_type'], 'time_weight')
        self.assertEqual(response.data['description'], 'Plank hold')
        self.assertEqual(float(response.data['weight']), -20.0)
        self.assertEqual(response.data['time_seconds'], 60)
        self.assertIsNone(response.data['reps'])
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
        
        # Verify exercise was saved to database
        exercise = Exercise.objects.get(id=response.data['id'])
        self.assertEqual(exercise.user, self.test_user)
        self.assertEqual(exercise.exercise_type, 'time_weight')
    
    def test_create_exercise_requires_authentication(self):
        """Test that creating an exercise requires authentication."""
        self._unauthenticate()
        data = {
            'exercise_type': 'reps_weight',
            'description': 'Test exercise',
            'weight': 50.0,
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_reps_weight_missing_reps(self):
        """Test that reps is required for reps_weight type."""
        self._authenticate()
        data = {
            'exercise_type': 'reps_weight',
            'description': 'Bench press',
            'weight': 100.5
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reps', response.data)
    
    def test_create_time_weight_missing_time(self):
        """Test that time_seconds is required for time_weight type."""
        self._authenticate()
        data = {
            'exercise_type': 'time_weight',
            'description': 'Plank hold',
            'weight': -20.0
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('time_seconds', response.data)
    
    def test_create_reps_weight_with_time_seconds_error(self):
        """Test that time_seconds should not be provided for reps_weight type."""
        self._authenticate()
        data = {
            'exercise_type': 'reps_weight',
            'description': 'Bench press',
            'weight': 100.5,
            'reps': 10,
            'time_seconds': 60
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('time_seconds', response.data)
    
    def test_create_time_weight_with_reps_error(self):
        """Test that reps should not be provided for time_weight type."""
        self._authenticate()
        data = {
            'exercise_type': 'time_weight',
            'description': 'Plank hold',
            'weight': -20.0,
            'time_seconds': 60,
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reps', response.data)
    
    def test_create_exercise_missing_description(self):
        """Test that description is required."""
        self._authenticate()
        data = {
            'exercise_type': 'reps_weight',
            'weight': 100.5,
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('description', response.data)
    
    def test_create_exercise_missing_weight(self):
        """Test that weight is required."""
        self._authenticate()
        data = {
            'exercise_type': 'reps_weight',
            'description': 'Bench press',
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('weight', response.data)
    
    def test_create_exercise_negative_weight(self):
        """Test that negative weight is allowed."""
        self._authenticate()
        data = {
            'exercise_type': 'time_weight',
            'description': 'Assisted pull-up',
            'weight': -30.5,
            'time_seconds': 45
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['weight']), -30.5)
    
    def test_create_exercise_invalid_exercise_type(self):
        """Test that invalid exercise_type is rejected."""
        self._authenticate()
        data = {
            'exercise_type': 'invalid_type',
            'description': 'Test exercise',
            'weight': 50.0,
            'reps': 10
        }
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('exercise_type', response.data)
    
    # GET EXERCISES TESTS
    
    def test_get_exercises_success(self):
        """Test successful retrieval of exercises."""
        self._authenticate()
        
        # Create some exercises for the test user
        Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='Exercise 1',
            weight=100.0,
            reps=10
        )
        Exercise.objects.create(
            user=self.test_user,
            exercise_type='time_weight',
            description='Exercise 2',
            weight=-20.0,
            time_seconds=60
        )
        
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['description'], 'Exercise 2')  # Newest first
        self.assertEqual(response.data[1]['description'], 'Exercise 1')
    
    def test_get_exercises_requires_authentication(self):
        """Test that getting exercises requires authentication."""
        self._unauthenticate()
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_exercises_empty_list(self):
        """Test getting exercises when user has none."""
        self._authenticate()
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)
    
    def test_get_exercises_user_isolation(self):
        """Test that users only see their own exercises."""
        self._authenticate()
        
        # Create exercise for test_user
        Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='My exercise',
            weight=100.0,
            reps=10
        )
        
        # Create exercise for other_user
        Exercise.objects.create(
            user=self.other_user,
            exercise_type='reps_weight',
            description='Other user exercise',
            weight=50.0,
            reps=8
        )
        
        # Get exercises as test_user
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'My exercise')
        self.assertEqual(float(response.data[0]['weight']), 100.0)
        
        # Switch to other_user and verify they see their own exercise
        self._authenticate(self.other_user)
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['description'], 'Other user exercise')
        self.assertEqual(float(response.data[0]['weight']), 50.0)
    
    def test_get_exercises_ordered_by_created_at(self):
        """Test that exercises are ordered by creation date (newest first)."""
        self._authenticate()
        
        # Create exercises in sequence
        exercise1 = Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='First exercise',
            weight=50.0,
            reps=10
        )
        exercise2 = Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='Second exercise',
            weight=60.0,
            reps=12
        )
        exercise3 = Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='Third exercise',
            weight=70.0,
            reps=15
        )
        
        response = self.client.get(self.get_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Should be ordered newest first
        self.assertEqual(response.data[0]['description'], 'Third exercise')
        self.assertEqual(response.data[1]['description'], 'Second exercise')
        self.assertEqual(response.data[2]['description'], 'First exercise')
    
    # GET SINGLE EXERCISE TESTS
    
    def test_get_exercise_success(self):
        """Test successful retrieval of a specific exercise by ID."""
        self._authenticate()
        
        # Create an exercise
        exercise = Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='Bench press',
            weight=100.0,
            reps=10
        )
        
        get_exercise_url = reverse('exercises:get_exercise', args=[exercise.id])
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], exercise.id)
        self.assertEqual(response.data['exercise_type'], 'reps_weight')
        self.assertEqual(response.data['description'], 'Bench press')
        self.assertEqual(float(response.data['weight']), 100.0)
        self.assertEqual(response.data['reps'], 10)
        self.assertIsNone(response.data['time_seconds'])
        self.assertIn('created_at', response.data)
        self.assertIn('updated_at', response.data)
    
    def test_get_exercise_time_weight_success(self):
        """Test successful retrieval of a time+weight exercise."""
        self._authenticate()
        
        # Create a time+weight exercise
        exercise = Exercise.objects.create(
            user=self.test_user,
            exercise_type='time_weight',
            description='Plank hold',
            weight=-20.0,
            time_seconds=60
        )
        
        get_exercise_url = reverse('exercises:get_exercise', args=[exercise.id])
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], exercise.id)
        self.assertEqual(response.data['exercise_type'], 'time_weight')
        self.assertEqual(response.data['description'], 'Plank hold')
        self.assertEqual(float(response.data['weight']), -20.0)
        self.assertEqual(response.data['time_seconds'], 60)
        self.assertIsNone(response.data['reps'])
    
    def test_get_exercise_requires_authentication(self):
        """Test that getting a specific exercise requires authentication."""
        self._unauthenticate()
        
        # Create an exercise
        exercise = Exercise.objects.create(
            user=self.test_user,
            exercise_type='reps_weight',
            description='Test exercise',
            weight=50.0,
            reps=10
        )
        
        get_exercise_url = reverse('exercises:get_exercise', args=[exercise.id])
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_exercise_not_found(self):
        """Test getting a non-existent exercise returns 404."""
        self._authenticate()
        
        # Try to get an exercise that doesn't exist
        get_exercise_url = reverse('exercises:get_exercise', args=[99999])
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Exercise not found')
    
    def test_get_exercise_user_isolation(self):
        """Test that users cannot access exercises belonging to other users."""
        self._authenticate()
        
        # Create an exercise for other_user
        other_exercise = Exercise.objects.create(
            user=self.other_user,
            exercise_type='reps_weight',
            description='Other user exercise',
            weight=50.0,
            reps=8
        )
        
        # Try to get other_user's exercise as test_user
        get_exercise_url = reverse('exercises:get_exercise', args=[other_exercise.id])
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Exercise not found')
        
        # Verify the exercise exists but belongs to other_user
        self.assertTrue(Exercise.objects.filter(id=other_exercise.id).exists())
        
        # Switch to other_user and verify they can access it
        self._authenticate(self.other_user)
        response = self.client.get(get_exercise_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], other_exercise.id)
        self.assertEqual(response.data['description'], 'Other user exercise')

