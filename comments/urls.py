from .views import CommentCreateView, CommentDetailAPIView, CommentUpdateAPIView, CommentDelete
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='commentCreate'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='commentDetail'),
    path('<int:pk>/edit/', CommentUpdateAPIView.as_view(), name='commentUpdate'),
    path('<int:pk>/delete/', CommentDelete.as_view(), name='commentDelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
