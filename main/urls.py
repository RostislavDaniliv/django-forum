from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    # path('register/', UserCreateAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('user/<slug:username>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('user/<slug:username>/edit/', UserUpdateAPIView.as_view(), name='user-update'),
    path('user/<slug:username>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('api/', include('rest_framework.urls')),
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('topic/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('topic/<int:pk>/edit/', PostUpdateAPIView.as_view(), name='post-update'),
    path('topic/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
    # path('api/user/', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)