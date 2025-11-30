# Fitness Tracker Django Boilerplate

This repository contains a Django project with JWT authentication and a login endpoint.

## Features

- Custom User model with id, username, email, password, and birthday
- JWT-based authentication
- Login endpoint supporting both username and email
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
├── fitness_tracker/      # Project settings
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL configuration
└── manage.py             # Django management script
```