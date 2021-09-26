from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=400, null=True, blank=True)
    intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    github_link = models.CharField(max_length=200, null=True, blank=True)
    twitter_link = models.CharField(max_length=200, null=True, blank=True)
    linkedin_link = models.CharField(max_length=200, null=True, blank=True)
    website_link = models.CharField(max_length=200, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
            
        return url

    def __str__(self):
        return str(self.user.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return str(self.name)

class Message(models.Model):
    sender = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    reciever = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ['is_read', '-creation_date']