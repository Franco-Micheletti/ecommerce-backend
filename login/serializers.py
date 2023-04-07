from rest_framework import serializers
from .models import CustomUser
          
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class UserSerializerPublicInfo(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id',
                  "profile_image_tag",
                  "username")