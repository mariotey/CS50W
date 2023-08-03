from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.CharField(max_length=64)
    content = models.CharField(max_length=64)
    created_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.creator}, {self.post_content}"

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=600)
    created_datetime = models.DateTimeField()
    likes = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True, related_name = "comments")

    def __str__(self):
        return f"{self.creator}, {self.content}, {self.created_datetime}"
