from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField()
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    image_url = models.CharField(max_length=500)
    start_bid = models.IntegerField()
    active_stat = models.BooleanField()  

    def __str__(self):
        return f"{self.title}, {self.description}, {self.start_bid}, {self.creator}"
    
class Bid(models.Model):
    list_title = models.CharField(max_length=64)
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.list_title}, {self.bidder_name}, {self.value}"

# class WatchList(models.Model):
#     list_title = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     watcher_name = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.list_title}, {self.watcher_name}"
    
# class Comment(models.Model):
#     commentor_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     listing = models.CharField(max_length=64)
#     comment = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{self.commentor_name}, {self.listing}"

class UserAssoc(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    bids = models.ManyToManyField(Bid, blank=True)
    # watchlists = models.ManyToManyField(Listing, blank=True)
    # comments = models.ManyToManyField(Comment, blank=True)

    # def __str__(self):
    #     return f"{self.username}, {self.bids}, {self.watchlists}, {self.comments}"

