from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', include('charities.urls')),
    path('admin/', admin.site.urls),
    path('about-us/', include('about_us.urls')),
    path('accounts/', include('accounts.urls')),
]
