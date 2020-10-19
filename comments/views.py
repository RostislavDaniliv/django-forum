from django.contrib.auth import get_user_model
from .permissions import ModerOnly, IsNotBanned, IsNotMuted
from .models import *
from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from .permissions import IsOwnerOrAdminOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .serializers import (
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentDetailSerializer,
    CommentDeleteSerializer,
)
User = get_user_model()


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny, IsNotBanned, IsNotMuted]


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly]

    def delete(self, request, pk, format=None):
        try:
            comment = Comment.objects.get(pk=pk)
            thread = comment.thread
            comment.delete()

            latest_comment = Comment.objects.filter(thread=thread).order_by('-created_at').first()

            if latest_comment is None:
                thread.last_activity = thread.created_at
            else:
                thread.last_activity = latest_comment.created_at
            thread.save()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly]


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [AllowAny]