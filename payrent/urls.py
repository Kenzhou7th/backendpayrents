from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RoomViewSet,
    TenantViewSet,
    NotificationViewSet,
    ReportViewSet,
    DashboardView,
    get_tenants_by_room,
    ForgotPasswordView,
    test_sms,
    get_room_count
)

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('rooms/<int:room_id>/tenants/', get_tenants_by_room, name='get-tenants-by-room'),
    path('test-sms/', test_sms),
    path('room-count/', get_room_count, name='room_count'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]