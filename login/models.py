from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Staff(models.Model):
    class DepartmentChoices(models.TextChoices):
        SALES = "Sales", "Sales"
        SUPPORT = "Support", "Support"
        MANAGEMENT = "Management", "Management"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(
        max_length=100, choices=DepartmentChoices.choices)
    # Adjusted max_length to accommodate hashed passwords
    hashed_password = models.CharField(max_length=128)

    def set_password(self, password):
        # Use Django's make_password to securely hash the password
        self.hashed_password = make_password(password)

    def check_password(self, password):
        # Use Django's check_password to verify the provided password
        return check_password(password, self.hashed_password)

    def __str__(self):
        return self.name
