from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.text import Truncator
from django.urls import reverse


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

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=2000, blank=True, default='')
    avatar = models.ImageField(upload_to='media', null=True, blank=True)
    is_moderator = models.BooleanField(default=False, verbose_name=("moderator"))
    is_ban = models.BooleanField(default=False)
    is_mute = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Topic(models.Model):
    title = models.CharField(max_length=2000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_creator")
    content = models.TextField()
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topic_moderator")
    status = models.CharField(choices=Status, max_length=20)
    slug = models.SlugField(max_length=500)

    def __str__(self):
        truncated_content = Truncator(self.content)
        return truncated_content.chars(30)


class Comment(models.Model):
    name = models.CharField(max_length=100, default='')
    text = models.TextField(max_length=5000, default='')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.topic}"