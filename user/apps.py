from django.apps import AppConfig
from user.signals import create_user_profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        post_save.connect(create_user_profile, sender=User)
