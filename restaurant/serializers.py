from rest_framework import serializers
from restaurant.models import Menu
from user.serializers import UserSerializer


class MenuSerializer(serializers.ModelSerializer):
    restaurant = UserSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = [
            "id",
            "restaurant",
        ]
