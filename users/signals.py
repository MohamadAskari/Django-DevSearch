from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail


def profileCreate(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )

        subject = 'Welcome'
        message = 'Good to see you!'

        send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [profile.email],
        fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    if created == False:
        profile = instance
        user = profile.user
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

def userDelete(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

post_save.connect(profileCreate, sender=User)
post_delete.connect(userDelete, sender=Profile)
post_save.connect(updateUser, sender=Profile)