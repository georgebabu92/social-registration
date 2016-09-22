from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models


class ProfileImage(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to="Profile_Image", null=True, blank=True)

    def __str__(self):
        return self.user.email


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = ProfileImage.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
