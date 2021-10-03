from django.contrib.auth.models import User
from django.test import TestCase
import random
import datetime
from django.db.models import Avg

from employee.models import Vote
from restaurant.models import Menu
from user.models import UserProfile


class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="user1", email="user1@gmail.com")
        self.userProfile1 = UserProfile.objects.get(user=self.user1)
        self.userProfile1.userType = "employee"
        self.userProfile1.save()

        self.user2 = User.objects.create(username="user2", email="user2@gmail.com")
        self.userProfile2 = UserProfile.objects.get(user=self.user2)
        self.userProfile2.userType = "employee"
        self.userProfile2.save()

        self.user3 = User.objects.create(username="user3", email="user3@gmail.com")
        self.userProfile3 = UserProfile.objects.get(user=self.user3)
        self.userProfile3.userType = "employee"
        self.userProfile3.save()

        self.restaurant1 = User.objects.create(username="restaurant1", email="restaurant1@gmail.com")
        self.userProfileRestaurant1 = UserProfile.objects.get(user=self.restaurant1)
        self.userProfileRestaurant1.userType = "restaurant"
        self.userProfileRestaurant1.save()
        self.menu1 = Menu.objects.create(restaurant=self.restaurant1, name="menu1")

        self.restaurant2 = User.objects.create(username="restaurant2", email="restaurant2@gmail.com")
        self.userProfileRestaurant2 = UserProfile.objects.get(user=self.restaurant2)
        self.userProfileRestaurant2.userType = "restaurant"
        self.userProfileRestaurant2.save()
        self.menu2 = Menu.objects.create(restaurant=self.restaurant2, name="menu2")

        self.restaurant3 = User.objects.create(username="restaurant3", email="restaurant3@gmail.com")
        self.userProfileRestaurant3 = UserProfile.objects.get(user=self.restaurant3)
        self.userProfileRestaurant3.userType = "restaurant"
        self.userProfileRestaurant3.save()
        self.menu3 = Menu.objects.create(restaurant=self.restaurant3, name="menu3")

    def test_user_is_typed_correctly(self):
        self.assertEqual(self.userProfile1.userType, "employee")
        self.assertEqual(self.userProfile2.userType, "employee")
        self.assertEqual(self.userProfile3.userType, "employee")

    def test_employee_voting(self):

        Vote.objects.create(menu=self.menu1, employee=self.user1, score=5.6)
        Vote.objects.create(menu=self.menu2, employee=self.user1, score=5.7)
        Vote.objects.create(menu=self.menu3, employee=self.user1, score=5.8)

        Vote.objects.create(menu=self.menu1, employee=self.user2, score=6.6)
        Vote.objects.create(menu=self.menu2, employee=self.user2, score=6.7)
        Vote.objects.create(menu=self.menu3, employee=self.user3, score=6.8)

        Vote.objects.create(menu=self.menu1, employee=self.user3, score=7.6)
        Vote.objects.create(menu=self.menu2, employee=self.user3, score=7.7)
        Vote.objects.create(menu=self.menu3, employee=self.user3, score=7.8)

        today = datetime.date.today()
        queryset = Vote.objects.filter(created__date=today).values('menu_id') \
            .annotate(avg_score=Avg('score')).order_by('-avg_score')

        self.assertEqual(queryset[0]['menu_id'], self.menu3.id)

