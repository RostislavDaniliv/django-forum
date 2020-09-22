from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

from .views import (
    # UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserDetailAPIView,
    UserListAPIView,
    UserDeleteAPIView,
    UserUpdateAPIView
)

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    # path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('<slug:username>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('<slug:username>/edit/', UserUpdateAPIView.as_view(), name='user-update'),
    path('<slug:username>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('api/', include('rest_framework.urls')),
    # path('api/user/', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)