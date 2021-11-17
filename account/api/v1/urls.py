from django.urls import path
from .views import signup, logout_view

from rest_framework.authtoken.views import obtain_auth_token


app_name = 'account.v1'


urlpatterns = [
    path('api/v1/login', obtain_auth_token, name='api-login'),
    path('api/v1/signup', signup, name='signup'),
    path('api/v1/logout', logout_view, name='logout'),
]

