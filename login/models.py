from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

class StaffManager(BaseUserManager):
    def create_user(self, email, name, department, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, department=department, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, department, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, department, password, **extra_fields)

class Staff(AbstractUser, PermissionsMixin):
    class DepartmentChoices(models.TextChoices):
        SALES = "Sales", "Sales"
        SUPPORT = "Support", "Support"
        MANAGEMENT = "Management", "Management"

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    department = models.CharField(
        max_length=100, choices=DepartmentChoices.choices)
    hashed_password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'  # Use email as the username
    REQUIRED_FIELDS = ['name', 'department']  # Add other required fields

    objects = StaffManager()

    def __str__(self):
        return self.name

    def create_jwt(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': self.pk,
        }

    def set_password(self, password):
        # Use Django's make_password to securely hash the password
        self.hashed_password = make_password(password)

    def check_password(self, password):
        # Use Django's check_password to verify the provided password
        return check_password(password, self.hashed_password)

    def __str__(self):
        return self.name