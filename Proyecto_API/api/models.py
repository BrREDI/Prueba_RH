from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Task(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=255)
    status=models.CharField(max_length=45)
    create_at=models.DateTimeField()
    update_at=models.DateTimeField()

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
