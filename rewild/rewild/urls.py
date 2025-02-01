"""
URL configuration for rewild project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
# URL Routing
from django.urls import path, include
from rest_framework.routers import DefaultRouter
import api.views

# Install dependencies:
# pip install django djangorestframework django-cors-headers pillow requests

# External API URL for recommendations
RECOMMENDATION_API_URL = "https://external-api.com/recommendations"


router = DefaultRouter()
router.register(r'mission_instances', api.views.MissionInstanceViewSet)
router.register(r'mission_types', api.views.MissionTypeViewSet)
router.register(r'complete_mission', api.views.DoneMissionViewSet)
router.register(r'profiles', api.views.UserProfileViewSet)
router.register(r'sightings', api.views.WildlifeSightingViewSet)
router.register(r'shop', api.views.ShopItemViewSet)
router.register(r'purchases', api.views.UserPurchaseViewSet)
router.register(r'locations', api.views.LocationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
