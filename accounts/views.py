from django.contrib.auth import get_user_model
from rest_framework import views
from .permissions import *
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
    UserLoginSerializer,
    UserTokenSerializer,
    UserDetailSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    UserCreateSerializer,
    GetBanSerializer,
    GetModerSerializer,
)

# View class to create user


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    throttle_scope = 'create_user'

# View class for detailed user information


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

# View class to remove user


class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'
    permission_classes = [IsOwnerOrAdminOrReadOnly]

# View class to update user information


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    throttle_scope = 'edit_user'

# View class to get a list of users


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

# View class for user authorization


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
            return Response({
                'token': token.key,
                'username': user.username,
                'name': user.profile.name,
                'is_staff': user.is_staff
            }, status=HTTP_200_OK)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# View class for logout user

class UserLogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)

# View the class to issue a ban to the user


class GetBanAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = GetBanSerializer
    permission_classes = [ModerOnly, IsAdminUser]

# View the class for issuing moderator rights to the user


class SetModerAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = GetModerSerializer
    permission_classes = [IsAdminUser]
