"""cornerCase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from user.urls import router as user_routers
from user.views import logout
from employee.urls import router as employee_routers
from restaurant.urls import router as restaurant_routers

router = DefaultRouter()
router.registry.extend(user_routers.registry)
router.registry.extend(employee_routers.registry)
router.registry.extend(restaurant_routers.registry)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^api/v1/', include(router.urls)),
                  url(r'^api/v1/logout$', logout, name="logout"),
                  path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
