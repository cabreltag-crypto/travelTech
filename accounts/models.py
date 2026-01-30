from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    travel_preferences = models.JSONField(null=True, blank=True)
    profile_completed = models.BooleanField(default=False)