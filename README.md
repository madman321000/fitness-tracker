# Fitness Tracker Django Boilerplate

This repository contains a Django project with JWT authentication and a login endpoint.

## Features

- Custom User model with id, username, email, password, and birthday
- JWT-based authentication
- Login endpoint supporting both username and email
- Exercise tracking with two types: reps+weight or time+weight
- Secure password hashing with salt
- Comprehensive unit tests

## Getting Started

### Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python fitness_tracker/manage.py migrate

# Create a superuser (optional, for admin access)
python fitness_tracker/manage.py createsuperuser
```

### Running the Server

```bash
python fitness_tracker/manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## Login Flow

### Creating a User

You can create a user in several ways:

#### Option 1: Django Admin (Recommended)
1. Start the server: `python fitness_tracker/manage.py runserver`
2. Visit http://127.0.0.1:8000/admin/
3. Login with your superuser credentials
4. Click on "Users" under "ACCOUNTS"
5. Click "Add User" and fill in the form

#### Option 2: Django Shell
```bash
python fitness_tracker/manage.py shell
```

Then in the shell:
```python
from accounts.models import User
from datetime import date

# Create a user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    birthday=date(1990, 1, 1)
)
```

### Testing the Login Endpoint

The login endpoint is available at: `POST /api/auth/login/`

#### Using cURL

**Login with username:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

**Login with email:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Expected Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Using Python requests

```python
import requests

url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "username": "testuser",  # or "email": "test@example.com"
    "password": "testpass123"
}

response = requests.post(url, json=data)
print(response.json())
```

#### Using Postman or similar tools

1. Method: `POST`
2. URL: `http://127.0.0.1:8000/api/auth/login/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
   ```json
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```

### Error Responses

- **Missing username/email**: `400 Bad Request` - "Username or email is required"
- **Missing password**: `400 Bad Request` - "Password is required"
- **Invalid credentials**: `401 Unauthorized` - "Invalid username/email or password"
- **Disabled account**: `401 Unauthorized` - "User account is disabled"

## Exercise Endpoints

The exercise endpoints allow authenticated users to create and retrieve exercises. Exercises can be one of two types:
- **Reps and Weight**: For exercises like bench press, squats, etc.
- **Time and Weight**: For exercises like planks, holds, etc.

**Note**: All exercise endpoints require JWT authentication. You must include the access token in the Authorization header.

### Creating an Exercise

The create endpoint is available at: `POST /api/exercises/create/`

#### Exercise Types

**Type 1: Reps and Weight**
- Requires: `exercise_type`, `description`, `weight`, `reps`
- Example: Bench press, squats, deadlifts

**Type 2: Time and Weight**
- Requires: `exercise_type`, `description`, `weight`, `time_seconds`
- Example: Plank holds, wall sits, weighted carries

**Note**: Weight can be positive or negative (e.g., -20.0 for bodyweight exercises with assistance).

#### Using cURL

**Create a reps+weight exercise:**
```bash
curl -X POST http://127.0.0.1:8000/api/exercises/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "exercise_type": "reps_weight",
    "description": "Bench press with proper form: Lie on bench, lower bar to chest, press up",
    "weight": 100.5,
    "reps": 10
  }'
```

**Create a time+weight exercise:**
```bash
curl -X POST http://127.0.0.1:8000/api/exercises/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "exercise_type": "time_weight",
    "description": "Plank hold: Maintain straight body position, engage core",
    "weight": -20.0,
    "time_seconds": 60
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "exercise_type": "reps_weight",
  "description": "Bench press with proper form: Lie on bench, lower bar to chest, press up",
  "weight": "100.50",
  "reps": 10,
  "time_seconds": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Using Python requests

```python
import requests

url = "http://127.0.0.1:8000/api/exercises/create/"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

# Create a reps+weight exercise
data = {
    "exercise_type": "reps_weight",
    "description": "Bench press with proper form",
    "weight": 100.5,
    "reps": 10
}

response = requests.post(url, json=data, headers=headers)
print(response.json())

# Create a time+weight exercise
data = {
    "exercise_type": "time_weight",
    "description": "Plank hold",
    "weight": -20.0,
    "time_seconds": 60
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### Getting All Exercises

The get endpoint is available at: `GET /api/exercises/`

This endpoint returns all exercises for the authenticated user, ordered by creation date (newest first).

#### Using cURL

```bash
curl -X GET http://127.0.0.1:8000/api/exercises/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": 2,
    "exercise_type": "time_weight",
    "description": "Plank hold: Maintain straight body position",
    "weight": "-20.00",
    "reps": null,
    "time_seconds": 60,
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  },
  {
    "id": 1,
    "exercise_type": "reps_weight",
    "description": "Bench press with proper form",
    "weight": "100.50",
    "reps": 10,
    "time_seconds": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

#### Using Python requests

```python
import requests

url = "http://127.0.0.1:8000/api/exercises/"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)
exercises = response.json()
print(exercises)
```

### Getting a Specific Exercise

The get endpoint for a specific exercise is available at: `GET /api/exercises/<exercise_id>/`

This endpoint returns a single exercise by ID. Users can only access their own exercises.

#### Using cURL

```bash
curl -X GET http://127.0.0.1:8000/api/exercises/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "id": 1,
  "exercise_type": "reps_weight",
  "description": "Bench press with proper form",
  "weight": "100.50",
  "reps": 10,
  "time_seconds": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Using Python requests

```python
import requests

exercise_id = 1
url = f"http://127.0.0.1:8000/api/exercises/{exercise_id}/"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)
exercise = response.json()
print(exercise)
```

**Error Responses:**
- **Exercise not found**: `404 Not Found` - "Exercise not found" (when exercise doesn't exist or belongs to another user)
- **Missing authentication**: `401 Unauthorized` - "Authentication credentials were not provided"

### Complete Example: Login and Create Exercise

```bash
# 1. Login to get JWT token
TOKEN=$(curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | grep -o '"access":"[^"]*' | cut -d'"' -f4)

# 2. Create an exercise using the token
curl -X POST http://127.0.0.1:8000/api/exercises/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "exercise_type": "reps_weight",
    "description": "Squats: Lower body until thighs parallel to floor, then stand up",
    "weight": 80.0,
    "reps": 12
  }'

# 3. Get all exercises
curl -X GET http://127.0.0.1:8000/api/exercises/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Get a specific exercise by ID (use the ID from step 2 response)
curl -X GET http://127.0.0.1:8000/api/exercises/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### Exercise Endpoint Error Responses

**Create Exercise (POST):**
- **Missing authentication**: `401 Unauthorized` - "Authentication credentials were not provided"
- **Invalid token**: `401 Unauthorized` - "Given token not valid for any token type"
- **Missing required fields**: `400 Bad Request` - Validation errors for missing fields
- **Invalid exercise_type**: `400 Bad Request` - "Invalid choice" (must be "reps_weight" or "time_weight")
- **Wrong fields for type**: `400 Bad Request` - e.g., "Reps is required for reps_weight type" or "Time should not be provided for reps_weight type"

**Get Exercises (GET all):**
- **Missing authentication**: `401 Unauthorized` - "Authentication credentials were not provided"
- **Invalid token**: `401 Unauthorized` - "Given token not valid for any token type"

**Get Exercise (GET by ID):**
- **Missing authentication**: `401 Unauthorized` - "Authentication credentials were not provided"
- **Invalid token**: `401 Unauthorized` - "Given token not valid for any token type"
- **Exercise not found**: `404 Not Found` - "Exercise not found" (when exercise doesn't exist or belongs to another user)

## Running Tests

### Run All Tests

```bash
python fitness_tracker/manage.py test
```

### Run Specific Test Suite

```bash
# Run all login tests
python fitness_tracker/manage.py test accounts.tests.LoginViewTests

# Run a specific test
python fitness_tracker/manage.py test accounts.tests.LoginViewTests.test_login_with_username_success
```

### Run Tests with Verbose Output

```bash
python fitness_tracker/manage.py test accounts.tests.LoginViewTests --verbosity=2
```

### Test Coverage

The test suite includes 13 test cases covering:
- Successful login with username and email
- Missing username/email errors
- Missing password errors
- Wrong password errors
- Invalid username/email errors
- Disabled user account errors
- Edge cases (users without email, username precedence, etc.)

## Project Structure

```
fitness_tracker/
├── accounts/              # Authentication app
│   ├── models.py         # User model
│   ├── views.py          # Login endpoint
│   ├── urls.py           # URL routing
│   └── tests.py          # Unit tests
├── exercises/             # Exercise tracking app
│   ├── models.py         # Exercise model
│   ├── views.py          # Exercise endpoints (GET, POST)
│   ├── serializers.py    # Exercise serializers
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin interface
├── fitness_tracker/      # Project settings
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL configuration
└── manage.py             # Django management script
```