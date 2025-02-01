import requests
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import MissionType, MissionInstance, UserProfile, WildlifeSighting, ShopItem, UserPurchase, Location, DoneMission
from .serializers import (MissionTypeSerializer,MissionInstanceSerializer, UserProfileSerializer,
                          WildlifeSightingSerializer, ShopItemSerializer, UserPurchaseSerializer, LocationSerializer)

RECOMMENDATION_API_URL = "https://external-api.com/recommendations"


class MissionTypeViewSet(viewsets.ModelViewSet):
    queryset = MissionType.objects.all()
    serializer_class = MissionTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class MissionInstanceViewSet(viewsets.ModelViewSet):
    queryset = MissionInstance.objects.all()
    serializer_class = MissionInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete_mission(self, request, *args, **kwargs):
        mission_instance = self.get_object()
        serializer = self.get_serializer(mission_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Image uploaded and DoneMission created"}, status=status.HTTP_201_CREATED)
        mission_instance.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class WildlifeSightingViewSet(viewsets.ModelViewSet):
    queryset = WildlifeSighting.objects.all()
    serializer_class = WildlifeSightingSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShopItemViewSet(viewsets.ModelViewSet):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserPurchaseViewSet(viewsets.ModelViewSet):
    queryset = UserPurchase.objects.all()
    serializer_class = UserPurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        user = request.user
        item_id = request.data.get('item_id')
        item = ShopItem.objects.get(id=item_id)
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        
        if user_profile.points >= item.price:
            user_profile.points -= item.price
            user_profile.save()
            UserPurchase.objects.create(user=user, item=item)
            return Response({"message": "Purchase successful!"})
        return Response({"error": "Not enough points."}, status=400)
