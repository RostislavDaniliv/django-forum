from django.contrib.auth import get_user_model
from .permissions import ModerOnly, IsNotBanned, IsNotMuted, IsModerHaveTopic
from .models import *
from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from .permissions import IsOwnerOrAdminOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

User = get_user_model()

from .serializers import (
    PostListSerializer,
    PostCreateSerializer,
    PostDetailSerializer,
    PostUpdateSerializer,
    PostDeleteSerializer,
    SetModerInTopicSerializer,
)


class PostListAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['title']


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, IsNotMuted, IsNotBanned]
    throttle_scope = 'create_post'


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsNotBanned]


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostDeleteSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly, IsNotBanned, IsModerHaveTopic]

    def delete(self, request, pk, format=None):
        try:
            post = Topic.objects.get(pk=pk)
            thread = post.thread
            post.delete()
            latest_post = Topic.objects.filter(thread=thread).order_by('-created_at').first()
            if latest_post is None:
                thread.last_activity = thread.created_at
            else:
                thread.last_activity = latest_post.created_at
            thread.save()
            return Response(status=HTTP_200_OK)

        except:
            return Response(status=HTTP_400_BAD_REQUEST)


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly, IsNotBanned, IsNotMuted, IsModerHaveTopic]


class SetModerInTopicAPIView(generics.UpdateAPIView):
    queryset = Topic.objects.all()
    serializer_class = SetModerInTopicSerializer
    permission_classes = [AllowAny]