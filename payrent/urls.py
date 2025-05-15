from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, TenantViewSet, NotificationViewSet, ReportViewSet, DashboardView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import get_tenants_by_room  # Import the function

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'reports', ReportViewSet)  # Fixed unmatched parenthesis

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Dashboard endpoint
    path('rooms/<int:room_id>/tenants/', get_tenants_by_room, name='get-tenants-by-room'),
]