from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('<int:pk>/edit/', PostUpdateAPIView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),
    path('<int:pk>/set_moder/', SetModerInTopicAPIView.as_view(), name='post-set_moder'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)