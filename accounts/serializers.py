from django.utils.timezone import now
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.humanize.templatetags.humanize import naturaltime
from .models import Profile

# Serializer for detailed output of user information


class UserDetailSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio')
    avatar = serializers.URLField(source='profile.avatar')
    name = serializers.CharField(source='profile.name')
    user = serializers.CharField(source='profile.profile')
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'user',
            'username',
            'name',
            'bio',
            'avatar',
            'is_staff',
            'date_joined',
        ]
        lookup_field = 'username'

    def get_date_joined(self, obj):
        return naturaltime(obj.date_joined)


# Serializer for displaying the list of users


class UserListSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio')
    avatar = serializers.URLField(source='profile.avatar')
    name = serializers.CharField(source='profile.name')

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'bio',
            'avatar',
            'is_staff',
            'date_joined'
        ]


# Serializer to update user information


class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', allow_blank=True)
    name = serializers.CharField(
    	source='profile.name',
    	max_length=32,
    	allow_blank=True
    )
    avatar = serializers.ImageField(source='profile.avatar', default='')
    email = serializers.EmailField(
        allow_blank=True,
        default='',
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='has already been taken by other user'
        )]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'bio',
            'avatar',
        )
        read_only_fields = ('username',)
        lookup_field = 'username'

    def update(self, instance, validated_data):
        try:
            username = self.context.get('request').user.username
        except:
            msg = _('Must be authenticated')
            raise serializers.ValidationError(msg, code='authorization')
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile
        for field, value in profile_data.items():
            if value:
                setattr(profile, field, value)

        for field, value in validated_data.items():
            if value:
                setattr(instance, field, value)

        profile.save()
        instance.save()
        return instance


# Serializer to create a user and profile


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        min_length=4,
        max_length=32,
        help_text=_(
            'Required. 4-32 characters. Letters, numbers, underscores or hyphens only.'
        ),
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='has already been taken by other user'
        )],
        required=True
    )
    password = serializers.CharField(
        min_length=4,
        max_length=32,
        write_only=True,
        help_text=_(
            'Required. 4-32 characters.'
        ),
        required=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='has already been taken by other user'
        )]
    )
    bio = serializers.CharField(source='profile.bio', allow_blank=True, default='')
    name = serializers.CharField(
        source='profile.name',
        allow_blank=True,
        default='',
        max_length=32
    )
    avatar = serializers.ImageField(source='profile.avatar', default='')

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'email',
            'password',
            'bio',
            'avatar',
        )

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(
                username=username,
                email=email
        )
        user.set_password(password)
        user.save()
        return user

# Serializer for assigning a token to a user


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# Serializer for user authorization


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=32,
        help_text=_(
            'Required. 32 characters or fewer. Letters, numbers, underscores or hyphens only.'
        ),
        required=True
    )
    token = serializers.CharField(allow_blank=True, read_only=True)
    name = serializers.CharField(source='profile.name', read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'password',
            'token',
        ]
        extra_kwargs = {"password": {"write_only": True}}


# Serializer for issuing a ban to the user


class GetBanSerializer(serializers.ModelSerializer):
    is_ban = serializers.BooleanField(default=False)

    class Meta:
        model = Profile
        fields = ['is_ban']
        read_only_fields=('is_ban',)
        lookup_field = 'username'

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile
        for field, value in profile_data.items():
            if value:
                setattr(profile, field, value)

        for field, value in validated_data.items():
            if value:
                setattr(instance, field, value)

        profile.save()
        instance.save()
        return instance


# Serializer for issuing moderator rights to the user


class GetModerSerializer(serializers.ModelSerializer):
    is_moderator = serializers.BooleanField(default=False)

    class Meta:
        model = Profile
        fields = ['is_moderator']
        read_only_fields = ('is_moderator',)
        lookup_field = 'username'

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        setattr(instance, 'updated_at', now())
        instance.save()
        return instance

