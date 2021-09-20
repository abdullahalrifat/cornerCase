from django.contrib import admin

# Register your models here.
from employee.models import Vote, RestaurantWinner

admin.site.register(Vote)
admin.site.register(RestaurantWinner)
