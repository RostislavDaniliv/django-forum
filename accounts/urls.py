from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='userList'),
    path('register/', UserCreateAPIView.as_view(), name='userRegister'),
    path('login/', UserLoginAPIView.as_view(), name='userLogin'),
    path('logout/', UserLogoutAPIView.as_view(), name='userLogout'),
    path('<slug:username>/', UserDetailAPIView.as_view(), name='userDetail'),
    path('<slug:username>/edit/', UserUpdateAPIView.as_view(), name='userUpdate'),
    path('<slug:username>/delete/', UserDeleteAPIView.as_view(), name='userDelete'),
    path('<int:pk>/ban/', GetBanAPIView.as_view(), name='userBan'),
    path('<int:pk>/moder/', SetModerAPIView.as_view(), name='userModer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)