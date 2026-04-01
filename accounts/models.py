from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('HR', 'HR Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def is_hr(self):
        return self.role == 'HR'

    def is_employee(self):
        return self.role == 'EMPLOYEE'

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
