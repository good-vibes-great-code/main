from django.contrib import admin
from .models import MissionType, MissionInstance, UserProfile, WildlifeSighting, ShopItem, UserPurchase, Location


admin.site.register(MissionType)
admin.site.register(MissionInstance)
admin.site.register(UserProfile)
admin.site.register(WildlifeSighting)
admin.site.register(ShopItem)
admin.site.register(UserPurchase)
admin.site.register(Location)
