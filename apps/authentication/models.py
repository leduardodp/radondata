from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='users', blank=True, null=True)

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username

