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

class Bids(models.Model):
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.listing.title}, {self.bidder_name}, {self.bid}"
    
# class Comments(models.Model):
#     commentor_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     listing = title = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=64)

#     def __str__(self):
#         return f"{self.id}, {self.creator}, {self.content}"

