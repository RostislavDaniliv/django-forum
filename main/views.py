from lib2to3.fixes.fix_input import context

from django.contrib.auth import get_user_model
from rest_framework import generics, views
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .permissions import IsOwnerOrAdminOrReadOnly, ModerOnly, IsNotBanned
from rest_framework.authtoken.models import Token
from .models import *

User = get_user_model()

from .serializers import (
    UserLoginSerializer,
    UserTokenSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
    CommentDetailSerializer,
    UserCreateSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostDetailSerializer,
    PostUpdateSerializer,
    PostDeleteSerializer,
    CommentDeleteSerializer,
    GetBanSerializer,
    GetModerSerializer,
)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    throttle_scope = 'create_user'


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    permission_classes = [IsOwnerOrAdminOrReadOnly]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    throttle_scope = 'edit_user'


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [AllowAny]


class UserLoginAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    throttle_scope = 'login'

    def post(self, request, *args, **kwargs):
        serializer = UserTokenSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            # return Response({
            #     'token': token.key,
            #     'username': user.username,
            #     'name': user.profile.name,
            #     'avatar': user.profile.avatar,
            #     'is_staff': user.is_staff
            # }, status=HTTP_200_OK)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

# topic

from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from .permissions import IsOwnerOrAdminOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response


class PostListAPIView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['title']


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'create_post'


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsNotBanned]

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = PostDeleteSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly]

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
    permission_classes = [IsOwnerOrAdminOrReadOnly, ModerOnly]


class GetBanAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = GetBanSerializer
    permission_classes = [ModerOnly, IsAdminUser]


class SetModerAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = GetModerSerializer
    permission_classes = [IsAdminUser]

# Comments


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer


class CommentDelete(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer
    permission_classes = [IsAuthenticated, ModerOnly]

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