from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Menu(models.Model):
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant_menu")
    name = models.CharField(max_length=100, null=False, blank=False)
    details = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='restaurant/menu/%Y/%m/%d', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'User Name : ' + self.name
