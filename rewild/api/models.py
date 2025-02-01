from django.contrib.auth.models import User
# from django.db import models
from django.contrib.gis.db import models

class Location(models.Model):  # Een erf OID 
    boundary = models.PolygonField(default="POLYGON(( 10 10, 10 20, 20 20, 20 15, 10 10))")

    
class MissionType(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    valid_date_start = models.DateTimeField()
    valid_date_end = models.DateTimeField()

    def __str__(self):
        return self.title

class DoneMission(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mission_type = models.ForeignKey(MissionType, on_delete=models.CASCADE)
    # gps_coordinates = #TODO
    latitude = models.FloatField()
    longitude = models.FloatField()
    completion_date = models.DateTimeField()
    image = models.ImageField()

class MissionInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission_type = models.ForeignKey(MissionType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    points = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.mission_type.title} (Expires: {self.expires_at})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)


class ShopItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()

class UserPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

#TODO look at.
class WildlifeSighting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    species_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='wildlife_sightings/')
    location = models.CharField(max_length=255, blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)