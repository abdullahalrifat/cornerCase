from rest_framework import serializers

from employee.models import Vote, RestaurantWinner
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from user.serializers import UserSerializer


class VoteSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = [
            "id",
            "employee",
            "menu",
        ]


class RestaurantWinnerSerializer(serializers.ModelSerializer):
    restaurant = UserSerializer(read_only=True)
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = RestaurantWinner
        fields = '__all__'
        read_only_fields = [
            "id",
            "restaurant",
            "menu",
        ]
