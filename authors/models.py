from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="", blank=True)

    def __str__(self):
        return f"{self.author.username}'s profile"
