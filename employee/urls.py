from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('employee', EmployeeViewSet, basename='employee')
router.register('employee-profile', EmployeeProfileViewSet, basename='employee-profile')
router.register('employee-get-menu', EmployeeMenuViewSet, basename='employee-get-menu')
router.register('employee-vote', EmployeeMenuVoteViewSet, basename='employee-vote')
router.register('restaurant-winner', RestaurantWinnerViewSet, basename='restaurant-winner')

urlpatterns = [

]
