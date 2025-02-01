from rest_framework import serializers
from .models import MissionType, MissionInstance, UserProfile, WildlifeSighting, ShopItem, UserPurchase, Location

class MissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionType
        fields = '__all__'

class MissionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionInstance
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class WildlifeSightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WildlifeSighting
        fields = '__all__'


class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = '__all__'

class UserPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPurchase
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

