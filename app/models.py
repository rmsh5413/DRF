from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    phonenumber = models.CharField(max_length=20, unique=True, blank=True, null=True)

    username = None

    USERNAME_FIELD = 'phonenumber'  # Use 'phonenumber' as the unique identifier for login
    REQUIRED_FIELDS = ['name', 'email']  # Add 'name' and 'email' to REQUIRED_FIELDS
   
    