from users.models import Profile
from django.contrib import admin
from .models import Message, Profile, Skill

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Message)