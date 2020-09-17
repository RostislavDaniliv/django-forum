from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


Status = (
    ('Draft', 'Draft'),
    ('Published', 'Published'),
    ('Close', 'Close'),
    ('Banned', 'Banned'),
)

USER_ROLES = (
    ('Admin', 'Admin'),
    ('Moderator', 'Moderator'),
    ('User', 'User'),
    ('Visitor', 'Visitor'),
    ('Banned', 'Banned'),
    ('Muted', 'Muted'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=2000, blank=True, default='')
    avatar = models.ImageField(upload_to='media', null=True, blank=True)
    user_role = models.CharField(choices=USER_ROLES, max_length=20)

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=2000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_creator")
    content = models.TextField()
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_moderator")
    status = models.CharField(choices=Status, max_length=20)
    slug = models.SlugField(max_length=500)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField(default='', null=True, blank=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_by")
    topic = models.ForeignKey(Topic, default='', on_delete=models.CASCADE, related_name="topic_comments")

    def __str__(self):
        return self.comment

