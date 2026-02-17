from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    # this method is used to create a regular user with email and password, and role can be specified as an extra field
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
# this method is used to create a superuser with admin privileges and role set to 'ADMIN'
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, password, **extra_fields)
    
# this is the custom user model that extends AbstractUser and uses email as the unique identifier instead of username. It also includes a role field to differentiate between admin, author, and reader users.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('AUTHOR', 'Author'),
        ('READER', 'Reader'),
    )
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='READER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_author(self):
        return self.role == 'AUTHOR'
    
    @property
    def is_reader(self):
        return self.role == 'READER'
    

