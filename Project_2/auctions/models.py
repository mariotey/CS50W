from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Comment(models.Model):
    commentor_name = models.ForeignKey(User, on_delete=models.CASCADE)
    list_title = models.CharField(max_length=64)
    comment = models.CharField(max_length=64)
    commented_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.commentor_name}, {self.list_title}"

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=500)
    bid_value = models.IntegerField(default=0)
    bid_counter = models.IntegerField(default=1)
    active_stat = models.BooleanField(default=True)  
    comments = models.ManyToManyField(Comment, blank=True, related_name = "comments")
    
    def __str__(self):
        return f"{self.title}, {self.description}, {self.bid_value}, {self.creator}"

class Bid(models.Model):
    listing = models.CharField(max_length=64)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.listing}, {self.bidder}, {self.value}"
    
class WatchList(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watcher_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.listing.title}, {self.watcher_name}"
    