from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import EventViewSet, UserLoginAPIView, UserLogoutAPIView, UserRegistrationAPIView

app_name = 'api-v1'

router = DefaultRouter()

router.register('events', EventViewSet, basename='event')

urlpatterns = [
    path("accounts/register", UserRegistrationAPIView.as_view(), name='account-register'),
    path("accounts/login", UserLoginAPIView.as_view(), name='account-login'),
    path("accounts/logout", UserLogoutAPIView.as_view(), name='account-logout'),
]

urlpatterns.extend(router.urls)
