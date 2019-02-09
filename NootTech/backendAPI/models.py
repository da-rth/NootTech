from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    colour = models.CharField(max_length=7, default="#00CCCC")

    def __str__(self):
        return self.username