from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Room, Tenant, Notification, Report

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'first_name', 'last_name', 'username',
            'contact_number', 'password', 'date_occupancy', 'room'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }

    def validate_room(self, value):
        if not Room.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Room does not exist")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'