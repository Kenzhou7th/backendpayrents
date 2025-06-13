from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payrent import views  # imong mga views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main app endpoints
    path('api/', include('payrent.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Password reset API endpoints
    path('api/password-reset/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/password-reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

    # SMS test endpoint
    path("test-sms/", views.test_sms, name="test_sms"),
]
