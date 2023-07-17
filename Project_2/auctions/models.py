from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=64)
    start_bid = models.IntegerField()
    active_stat = models.BooleanField()  

    def __str__(self):
        return f"{self.title}, {self.description}, {self.start_bid}, {self.creator}"

class Bids(models.Model):
    bidder_name = models.CharField(max_length=64, primary_key=True)
    title = models.CharField(max_length=64)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.title}, {self.bidder_name}, {self.bid}"
    
class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    list_title = models.CharField(max_length=64)
    creator = User.username
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}, {self.creator}, {self.content}"

