from django.urls import path
from .views import UserRegisterAPIViews
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('registration/', UserRegisterAPIViews.as_view(), name='user-registration'),
    path('login/', obtain_auth_token, name='user-obtain_auth_token'),
]