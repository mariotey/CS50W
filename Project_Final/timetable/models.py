from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    user_image = models.TextField(blank=True)

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=600)
    event_description = models.CharField(max_length=6000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name}, {self.start_date}, {self.end_date}"

class Holiday(models.Model):
    name = models.CharField(max_length=600)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name}, {self.start_date}, {self.end_date}"
