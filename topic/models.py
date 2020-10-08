from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.text import Truncator

User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    title = models.CharField(max_length=2000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_creator")
    content = models.TextField()
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_moderator")
    slug = models.SlugField(max_length=500)

    def __str__(self):
        truncated_content = Truncator(self.content)
        return truncated_content.chars(30)