from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

pass

# urlpatterns = [
    # path('', UserListAPIView.as_view(), name='user-list'),
    # path('register/', UserCreateAPIView.as_view(), name='user-register'),
    # path('user/login/', UserLoginAPIView.as_view(), name='user-login'),
    # path('user/logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    # path('user/<slug:username>/', UserDetailAPIView.as_view(), name='user-detail'),
    # path('user/<slug:username>/edit/', UserUpdateAPIView.as_view(), name='user-update'),
    # path('user/<slug:username>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),
    # path('user/<int:pk>/ban/', GetBanAPIView.as_view(), name='user-ban'),
    # path('user/<int:pk>/moder/', SetModerAPIView.as_view(), name='user-moder'),
    # path('api/', include('rest_framework.urls')), ----???
    # path('topic/create/', PostCreateAPIView.as_view(), name='post-create'),
    # path('topic/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    # path('topic/<int:pk>/edit/', PostUpdateAPIView.as_view(), name='post-update'),
    # path('topic/<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
    # path('topic/<int:pk>/set_moder/', SetModerInTopicAPIView.as_view(), name='post-set_moder'),
    # path('comment/create/', CommentCreateView.as_view(), name='comment-create'),
    # path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    # path('comment/<int:pk>/edit/', CommentUpdateAPIView.as_view(), name='comment-update'),
    # path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment-delete'),
    # path('api/user/', include('main.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)