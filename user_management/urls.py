from django.contrib import admin
from django.urls import path
from user_management import views
from rest_framework.routers import DefaultRouter
from user_management.views import RoleModelViewSet, RegistrationUserModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'roles', RoleModelViewSet, basename='role')
router.register(r'registration', RegistrationUserModelViewSet)
router.register(r'', UserModelViewSet)

urlpatterns = [
    path('hello/', views.hello),
    path('send_email/', views.mail_test)
] + router.urls
