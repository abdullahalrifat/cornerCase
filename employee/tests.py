from django.contrib.auth.models import User
from django.test import TestCase
import random
# Create your tests here.
from employee.models import Vote
from restaurant.models import Menu
from user.models import UserProfile


class employeeTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1", email="user1@gmail.com")
        userProfile1 = UserProfile.objects.get(user=user1)
        userProfile1.userType = "employee"
        userProfile1.save()
        user2 = User.objects.create(username="user2", email="user2@gmail.com")
        userProfile2 = UserProfile.objects.get(user=user2)
        userProfile2.userType = "employee"
        userProfile2.save()
        user3 = User.objects.create(username="user3", email="user3@gmail.com")
        userProfile3 = UserProfile.objects.get(user=user3)
        userProfile3.userType = "employee"
        userProfile3.save()

        restaurant1 = User.objects.create(username="restaurant1", email="restaurant1@gmail.com")
        userProfileRestaurant1 = UserProfile.objects.get(user=restaurant1)
        userProfileRestaurant1.userType = "restaurant"
        userProfileRestaurant1.save()
        menu1 = Menu.objects.create(restaurant=restaurant1, name="menu1")
        restaurant2 = User.objects.create(username="restaurant2", email="restaurant2@gmail.com")
        userProfileRestaurant2 = UserProfile.objects.get(user=restaurant2)
        userProfileRestaurant2.userType = "restaurant"
        userProfileRestaurant2.save()
        menu2 = Menu.objects.create(restaurant=restaurant2, name="menu1")

        restaurant3 = User.objects.create(username="restaurant3", email="restaurant3@gmail.com")
        userProfileRestaurant3 = UserProfile.objects.get(user=restaurant3)
        userProfileRestaurant3.userType = "restaurant"
        userProfileRestaurant3.save()
        menu3 = Menu.objects.create(restaurant=restaurant3, name="menu1")

    def employee_voting(self):
        users = User.objects.all()
        menus = Menu.objects.all()
        for user in users:
            if len(UserProfile.objects.get(userType="employee")):
                for menu in menus:
                    score = random.uniform(1, 10)
                    print(user.username + " voting for " + menu.name + " score=" + score)
                    Vote.objects.create(menu=menu, employee=user, score=score)
