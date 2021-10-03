from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.
from restaurant.models import Menu


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_vote")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_vote")
    score = models.FloatField(default=0.00, validators=[MinValueValidator(0.00), MaxValueValidator(10.00)])
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Employee: ' + self.employee.username + '- Menu : ' + self.menu.name + '- Score: ' + str(self.score)


class RestaurantWinner(models.Model):
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant_winner")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_winner")
    avg_score = models.FloatField(default=0.00, validators=[MinValueValidator(0.00), MaxValueValidator(10.00)])
    winning_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Restaurant: ' + self.restaurant.username + '- Date : ' + str(self.winning_date)
