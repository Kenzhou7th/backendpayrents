from rest_framework import serializers
from .models import Room, Tenant, Notification, Report  # Import the Report model

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class TenantSerializer(serializers.ModelSerializer):
    billingHistory = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = '__all__'

    def get_billingHistory(self, obj):
        # Example: Return dummy billing history
        return [
            {
                "billingId": 1,
                "dueDate": "2025-05-15",
                "rentFee": 5000,
                "waterBill": 500,
                "electricBill": 1000,
                "status": "Unpaid",
            }
        ]

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# Add the ReportSerializer
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'