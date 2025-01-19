from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/users", null=True, blank=True)

    def __str__(self):
        return self.username
    
class Contact(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    telegram = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
