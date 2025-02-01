from rest_framework import serializers
from datetime import datetime
from .models import MissionType, MissionInstance, UserProfile, WildlifeSighting, ShopItem, UserPurchase, Location

class MissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionType
        fields = '__all__'

class MissionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionInstance
        fields = '__all__'

    def extract_gps(self, image):
        """Extracts GPS metadata from the uploaded image."""
        try:
            img = Image.open(image)
            exif_data = img._getexif()

            if not exif_data:
                return None  # No EXIF data

            gps_info = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    for t in value:
                        sub_tag = GPSTAGS.get(t, t)
                        gps_info[sub_tag] = value[t]

            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat = gps_info["GPSLatitude"]
                lon = gps_info["GPSLongitude"]
                
                lat_ref = gps_info.get("GPSLatitudeRef", "N")
                lon_ref = gps_info.get("GPSLongitudeRef", "E")
                
                # Convert to decimal degrees
                latitude = self.convert_to_degrees(lat)
                longitude = self.convert_to_degrees(lon)

                if lat_ref != "N":
                    latitude = -latitude
                if lon_ref != "E":
                    longitude = -longitude

                return latitude, longitude
        except Exception as e:
            print(f"Error extracting GPS: {e}")
        return None

    def convert_to_degrees(self, value):
        """Helper function to convert GPS coordinates to decimal format."""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)

    def create(self, validated_data):
        """Creates a DoneMission instance from the uploaded image."""
        image = validated_data.pop('image')
        gps_coords = self.extract_gps(image)

        if gps_coords:
            latitude, longitude = gps_coords
            DoneMission.objects.create(
                location = self.fields.user.location,
                mission_type = self.fields.mission_type,
                latitude=latitude,
                longitude=longitude,
                completion_date = datetime.now(),
                image = image
            )

        return super().create(validated_data)

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

