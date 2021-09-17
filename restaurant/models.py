from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Menu(models.Model):
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")
    name = models.CharField(max_length=100, null=False, blank=False)
    details = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='restaurant/menu/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'User Name : ' + self.name
