from django.urls import path, include
from about_us.views import about_us

app_name = 'about_us'

urlpatterns = [
    path('', about_us, name='about_us'),

]
