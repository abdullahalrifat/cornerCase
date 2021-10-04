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
from .permissions import IsEmployee, IsSuperAdmin
from .serializers import VoteSerializer, RestaurantWinnerSerializer


# EmployeeViewSet to handle Employee create,update,delete,list
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
            serialized.save(userType="employee")

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


# EmployeeProfileViewSet to store additional information like userType='employee'
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


# EmployeeMenuViewSet to view daily menu uploaded by restaurants
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
        if self.action in ['update']:
            self.permission_classes = [IsSuperAdmin, ]
        elif self.action in ['destroy']:
            self.permission_classes = [IsSuperAdmin, ]
        elif self.action in ['list']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [IsSuperAdmin, ]
        if self.action in ['destroy']:
            self.permission_classes = [IsSuperAdmin, ]
        return super().get_permissions()

    def list(self, request):
        today = datetime.date.today()
        menu = Menu.objects.filter(created__date=today)
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# checking if specific time between two times or not
def is_now_in_time_period(start_time, end_time, now_time):
    if start_time < end_time:
        return start_time <= now_time <= end_time
    else:
        # Over midnight:
        return now_time >= start_time or now_time <= end_time


# EmployeeMenuVoteViewSet to handle Employee voting system
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
        # checking if current request time is between 11AM - 12 PM
        # as Employees meant to vote before going for Lunch i am considering 12PM is last voting time
        # so our voting slot will be open from 11AM - 12PM
        if is_now_in_time_period(datetime.time(11, 00), datetime.time(12, 00), datetime.datetime.now().time()):
            menu_id = request.data.get("menu")
            menu = get_object_or_404(Menu, id=menu_id, created__date=today)
            try:
                # for specific menu employee can vote only once
                # so checking if employee has already voted or not
                # if already voted till 12PM employee can update his voting score
                vote = Vote.objects.get(created__date=today, menu=menu, employee=request.user)
                serializer = VoteSerializer(instance=vote, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                vote = VoteSerializer(vote)
                return Response({'Success': "Vote Updated Successful", "menu_details": vote.data},
                                status=status.HTTP_202_ACCEPTED)
            except Vote.DoesNotExist:
                # if not votes creating new voting object
                serialized = VoteSerializer(data=request.data)
                if serialized.is_valid():
                    vote = serialized.save(employee=request.user, menu=menu)
                    vote = VoteSerializer(vote)
                    return Response({'Success': "Vote Casted Successful", "menu_details": vote.data},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if vote request time is not between 11AM - 12PM informing user
            return Response("Lunch Time Finished, Try Between 11:00 AM - 12:00 PM",
                            status=status.HTTP_406_NOT_ACCEPTABLE)


# RestaurantWinnerViewSet to handle winner for daily voting system
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
            # checking if already a winner is determined or not
            # if already a winner has been selected return that information
            winner = RestaurantWinner.objects.get(created__date=today)
            serializer_class = RestaurantWinnerSerializer(winner)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except RestaurantWinner.DoesNotExist:
            print("Not Calculated Yet")

        # As 12PM is last voting time so after from 12:10 till 11:59 PM we are calculation that day's result
        # so checking if request time is between 12:10PM - 11:59 PM or not
        if is_now_in_time_period(datetime.time(12, 10), datetime.time(23, 59), datetime.datetime.now().time()):
            # From all the voting responses filtering Votes for today
            # Grouping All the Data by menu_id and calculation average of that specific vote score
            # sorting all the data depending on that avg_score
            # That means First menu of the list is our winner of that specific day
            queryset = Vote.objects.filter(created__date=today).values('menu_id') \
                .annotate(avg_score=Avg('score')).order_by('-avg_score')

            if len(queryset) == 0:
                # if no data found that means no voting happened today
                return Response("No Voting Happened Today", status=status.HTTP_200_OK)

            # getting all the winner's list from beginning
            winner_list = RestaurantWinner.objects.filter().order_by('-created__date')
            # by default winner is the first menu of the queryset
            final_winner = Menu.objects.get(id=queryset[0]['menu_id'])
            avg_score = queryset[0]['avg_score']
            # print(queryset)
            # checking if at-least before today we have 2 more days winner data
            if len(winner_list) > 2:
                # if there is winner's data for more than 2 days
                # we need to check make sure the winner should not be winner for 3 consecutive days
                # from today's calculated score for menus,
                # for each menu from max avg score to low avg score
                # if that menu's restaurant have also became winner for last 2 days or not
                for menu in queryset:
                    menu_obj = Menu.objects.get(id=menu['menu_id'])
                    if winner_list[0].menu.restaurant.id != menu_obj.restaurant.id and \
                            winner_list[1].menu.restaurant.id != menu_obj.restaurant.id:
                        final_winner = Menu.objects.get(id=menu['menu_id'])
                        avg_score = winner_list[0].avg_score
                        break
            else:
                # if not then the winner is the first menu from the queryset
                # so getting the menu object and avg score
                final_winner = Menu.objects.get(id=queryset[0]['menu_id'])
                avg_score = queryset[0]['avg_score']
            # storing the winner data for current day
            winner_obj = RestaurantWinner.objects.create(menu=final_winner,
                                                         restaurant=final_winner.restaurant,
                                                         avg_score=avg_score, winning_date=today)
            serializer_class = RestaurantWinnerSerializer(winner_obj)
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        else:
            # if request made between 12AM-12PM then there is still voting time left
            return Response("There is Still Voting Time Left, Try Between 12:10 PM - 11:59 AM",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
