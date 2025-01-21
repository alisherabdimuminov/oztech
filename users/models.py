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
    profession = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/users", null=True, blank=True)

    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
    

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Contact(models.Model):
    name = models.CharField(max_length=1000)
    phone = models.CharField(max_length=1000)
    telegram = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Date(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey("courses.course", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    ended = models.DateField()

    def __str__(self):
        return str(self.created)
