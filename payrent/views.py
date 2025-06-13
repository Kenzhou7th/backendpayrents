from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Room, Tenant, Notification, Report
from .serializers import RoomSerializer, TenantSerializer, NotificationSerializer, ReportSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.sms import send_sms

@api_view(['GET'])
def test_sms(request):
    response = send_sms("09977500849", "Test SMS from PayRent.")
    return Response(response)

# Room ViewSet
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for testing

    def create(self, request, *args, **kwargs):
        print("Incoming request data:", request.data)  # Log the incoming data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Log validation errors
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

# Tenant ViewSet
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

#@api_view(['GET'])
def get_tenants_by_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        tenants = room.tenants.all()  # Use the related_name defined in the ForeignKey
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# Report ViewSet
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

# Dashboard View
class DashboardView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def get(self, request):
        # Aggregate data for the dashboard
        total_rooms = Room.objects.count()
        active_tenants = Tenant.objects.count()
        pending_reports = Report.objects.filter(description__icontains="pending").count()

        # Return the aggregated data
        data = {
            "total_rooms": total_rooms,
            "active_tenants": active_tenants,
            "pending_reports": pending_reports,
        }
        return Response(data)

# Forgot Password View
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # Generate a password reset link (example only, replace with actual logic)
            reset_link = f"http://your-frontend-url/reset-password/{user.id}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@yourdomain.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)


