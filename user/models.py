from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name="profile")
    mobile = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    gender = models.CharField(max_length=100, null=False, blank=False)
    userType = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='user/photo', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'User Name : ' + self.user.username
