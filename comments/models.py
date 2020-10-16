from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from topic.models import Topic


class Comment(models.Model):
    name = models.CharField(max_length=100, default='')
    text = models.TextField(max_length=5000, default='')
    parent = models.ForeignKey(
    'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.topic}"
