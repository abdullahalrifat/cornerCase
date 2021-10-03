from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('restaurant', RestaurantViewSet, basename='restaurant')
router.register('restaurant-profile', RestaurantProfileViewSet, basename='restaurant-profile')
router.register('restaurant-menu', MenuViewSet, basename='menu')

urlpatterns = [

]
