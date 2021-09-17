from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
from restaurant.models import Menu


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    score = models.DecimalField(max_digits=2, decimal_places=2, default=Decimal(0.00))
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Employee: ' + self.employee.username + '- Menu : ' + self.menu.name + '- Score: ' + str(self.score)


class RestaurantWinner(models.Model):
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")
    avg_score = models.DecimalField(max_digits=2, decimal_places=2, default=Decimal(0.00))
    winning_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Restaurant: ' + self.restaurant.username + '- Date : ' + str(self.winning_date)
