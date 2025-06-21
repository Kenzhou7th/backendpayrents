from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payrent.views import (
    ForgotPasswordView,
    ResetPasswordConfirmView,
    test_sms,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main app endpoints
    path('api/', include('payrent.urls')),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Corrected Password reset endpoints
    path('api/password-reset/', ForgotPasswordView.as_view(), name='password_reset'),
    path('api/password-reset/confirm/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),

    # SMS test
    path("test-sms/", test_sms, name="test_sms"),
]
