from django.db.models import Avg
import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# Create your views here.
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from user.models import UserProfile
from user.serializers import UserSerializer, UserProfileSerializer
from user.permissions import IsOwnerOrAdmin
from .models import Vote, RestaurantWinner
from .permissions import IsEmployee
from .serializers import VoteSerializer, RestaurantWinnerSerializer


class EmployeeViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update']:
            self.permission_classes = [IsOwnerOrAdmin, ]
        elif self.action in ['destroy', 'list']:
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def create(self, request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            user = serialized.save(userType="employee")

            return Response("Employee created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = UserProfile.objects.filter(userType="employee")
        serializer_class = UserProfileSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeProfileViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):
        if self.action in ['update']:
            self.permission_classes = [IsOwnerOrAdmin, ]
        elif self.action in ['destroy', 'list']:
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def list(self, request):
        queryset = UserProfile.objects.all(userType="employee")
        serializer_class = UserProfileSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(UserProfile, id=pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(UserProfile, id=pk)
        serializer = UserProfileSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeMenuViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'list']:
            self.permission_classes = [permissions.IsAuthenticated, ]
        return super().get_permissions()

    def list(self, request):
        today = datetime.date.today()
        menu = Menu.objects.filter(created__date=today)
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def is_now_in_time_period(start_time, end_time, now_time):
    if start_time < end_time:
        return now_time >= start_time and now_time <= end_time
    else:
        # Over midnight:
        return now_time >= start_time or now_time <= end_time


class EmployeeMenuVoteViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsEmployee, ]
        return super().get_permissions()

    def create(self, request):
        today = datetime.date.today()
        if is_now_in_time_period(datetime.time(00, 00), datetime.time(12, 00), datetime.datetime.now().time()):
            menu_id = request.data.get("menu")
            menu = get_object_or_404(Menu, id=menu_id, created__date=today)
            try:
                vote = Vote.objects.get(created__date=today, menu=menu, employee=request.user)
                serializer = VoteSerializer(instance=vote, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                vote = VoteSerializer(vote)
                return Response({'Success': "Vote Updated Successful", "menu_details": vote.data},
                                status=status.HTTP_202_ACCEPTED)
            except Vote.DoesNotExist:
                serialized = VoteSerializer(data=request.data)
                if serialized.is_valid():
                    vote = serialized.save(employee=request.user, menu=menu)
                    vote = VoteSerializer(vote)
                    return Response({'Success': "Vote Casted Successful", "menu_details": vote.data},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Lunch Time Finished, Try Between 12:00 AM - 12:00 PM",
                            status=status.HTTP_406_NOT_ACCEPTABLE)


class RestaurantWinnerViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = RestaurantWinner.objects.all()
    serializer_class = RestaurantWinnerSerializer

    def get_permissions(self):
        if self.action in ['update']:
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.action in ['destroy']:
            self.permission_classes = [permissions.IsAdminUser, ]
        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def list(self, request):
        today = datetime.date.today()
        try:
            winner = RestaurantWinner.objects.get(created__date=today)
            serializer_class = RestaurantWinnerSerializer(winner)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except RestaurantWinner.DoesNotExist:
            print("Not Calculated Yet")

        if is_now_in_time_period(datetime.time(12, 00), datetime.time(1, 59), datetime.datetime.now().time()):
            queryset = Vote.objects.filter(created__date=today).values('menu_id') \
                .annotate(avg_score=Avg('score')).order_by('-avg_score')
            winner_list = RestaurantWinner.objects.filter().order_by('-created__date')
            final_winner = None
            avg_score = None
            if len(winner_list) > 2:
                for menu in queryset:
                    if winner_list[0].menu.id != menu['menu_id'] and winner_list[1].menu.id != menu['menu_id']:
                        final_winner = Menu.objects.get(id=menu['menu_id'])
                        avg_score = winner_list[0].avg_score
                        break
            else:
                final_winner = Menu.objects.get(id=queryset[0]['menu_id'])
                avg_score = queryset[0]['avg_score']

            winner_obj, winner = RestaurantWinner.objects.create(menu=final_winner,
                                                                 restaurant=final_winner.restaurant,
                                                                 avg_score=avg_score, winning_date=today)
            serializer_class = RestaurantWinnerSerializer(winner_obj)
            print(serializer_class.data)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            return Response("There is Still Voting Time Left, Try Between 12:00 PM - 12:00 AM",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
