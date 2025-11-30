from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom user manager for User model."""
    
    def create_user(self, username, email=None, password=None, birthday=None, **extra_fields):
        """Create and save a regular user."""
        if not username:
            raise ValueError('The Username field must be set')
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, birthday=birthday, **extra_fields)
        user.set_password(password)  # This handles hashing and salting
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, birthday=None, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, birthday, **extra_fields)


class User(AbstractBaseUser):
    """Custom User model with id, username, email, password, and birthday."""
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)  # Django stores hashed password here
    birthday = models.DateField(null=True, blank=True)
    
    # Required fields for Django admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission."""
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        """Check if user has permissions to view the app."""
        return self.is_superuser
