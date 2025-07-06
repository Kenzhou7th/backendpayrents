from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import Room, Tenant, Notification, Report
from .serializers import RoomSerializer, TenantSerializer, NotificationSerializer, ReportSerializer
from .utils.sms import send_sms
import logging


logger = logging.getLogger(__name__)


# ✅ TEST SMS ENDPOINT
@api_view(['GET'])
def test_sms(request):
    phone_number = request.query_params.get('phone_number', '09977500849')  # Default value
    message = request.query_params.get('message', 'Test SMS from PayRent.')  # Default value
    response = send_sms(phone_number, message)
    return Response(response)


# ✅ ROOMS
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info("Incoming request data: %s", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Validation errors: %s", serializer.errors)
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


# ✅ TENANTS
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


@api_view(['GET'])
def get_tenants_by_room(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        tenants = room.tenants.all()
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ✅ NOTIFICATIONS
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


# ✅ REPORTS
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


# ✅ DASHBOARD DATA PER BRANCH (FIXED)
class DashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        branch = request.query_params.get('branch')
        if not branch:
            return Response({'error': 'Branch is required'}, status=status.HTTP_400_BAD_REQUEST)

        total_rooms = Room.objects.filter(branch=branch).count()
        tenants = Tenant.objects.filter(room__branch=branch)
        total_reports = Report.objects.filter(room__branch=branch).count()
        payment_this_month = tenants.aggregate(total=Sum('total_payment'))['total'] or 0
        tenants_paid_this_month = tenants.filter(is_paid=True).count()

        data = {
            "total_rooms": total_rooms,
            "total_tenants": tenants.count(),
            "payment_this_month": payment_this_month,
            "total_reports": total_reports,
            "active_tenants": tenants.count(),
            "tenants_paid_this_month": tenants_paid_this_month,
        }
        return Response(data)


# ✅ PASSWORD RESET (STEP 1) – Send Reset Link
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = f"http://localhost:3000/reset-password?uid={uid}&token={token}"  # replace with frontend URL

            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'noreply@yourdomain.com',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)


# ✅ PASSWORD RESET (STEP 2) – Confirm Reset and Save New Password
class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not all([uid, token, new_password]):
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, DjangoUnicodeDecodeError):
            return Response({'error': 'Invalid user or UID'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_room_count(request):
    permission_classes = [IsAuthenticated]  # Restrict access
    total_rooms = Room.objects.count()
    return JsonResponse({'total_rooms': total_rooms})
