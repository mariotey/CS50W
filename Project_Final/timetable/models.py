from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    event_name = models.CharField(max_length=600)
    event_description = models.CharField(max_length=6000)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.user}, {self.event_name}"

class Holiday(models.Model):
    holiday_name = models.CharField(max_length=600)
    holiday_description = models.CharField(max_length=6000)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.holiday_name}, {self.date}"
