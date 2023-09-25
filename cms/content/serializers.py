from .models import contents
from rest_framework import serializers


class AllContentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email')
    class Meta:
        model = contents
        fields = ['title','user_email']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = contents
        fields = '__all__'