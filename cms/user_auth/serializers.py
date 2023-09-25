from rest_framework import serializers 
from .models import role,rootUser


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = role
        fields = "__all__"


class AllUserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name')
    class Meta:
        model = rootUser
        fields = ['email','phone','role_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = rootUser
        fields = "__all__"
        
        
    def create(self, validated_data):
        return rootUser.objects.create_user(**validated_data)    

class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = rootUser
        fields = ('email','password', 'token')

        read_only_fields = ['token']
