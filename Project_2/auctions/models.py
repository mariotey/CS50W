from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=64)
    start_bid = models.IntegerField()
    active_stat = models.BooleanField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, {self.description}, {self.start_bid}, {self.creator}"

class Bids(models.Model):
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.bid}"
    
class Comments(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.description}"

