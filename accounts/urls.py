from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views import UserRegistration, LogoutAPIView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration', include('dj_rest_auth.registration.urls'))
]
