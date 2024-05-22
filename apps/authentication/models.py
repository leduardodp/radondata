from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from core.settings import  STATIC_URL , MEDIA_URL


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.email