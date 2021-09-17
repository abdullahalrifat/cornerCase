from django.db import models
from django.db.models import JSONField

from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
def get_unique_slug(model, field_name, value):
    max_length = model._meta.get_field(field_name).max_length
    slug = slugify(value)
    num = 1
    unique_slug = '{}-{}'.format(slug[:max_length - len(str(num)) - 1], num)
    while model.objects.filter(**{field_name: unique_slug}).exists():
        unique_slug = '{}-{}'.format(slug[:max_length - len(str(num)) - 1], num)
        num += 1
    return unique_slug


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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
