from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.timezone import now
from .models import Topic
from main.models import UserProfile

# USERS


class UserDetailSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio')
    avatar = serializers.URLField(source='profile.avatar')
    status = serializers.URLField(source='profile.status')
    name = serializers.CharField(source='profile.name')
    threads = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='thread-detail',
        lookup_field='pk'
    )
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail',
        lookup_field='pk'
    )
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'bio',
            'avatar',
            'status',
            'is_staff',
            'date_joined',
            'threads',
            'posts'
        ]
        lookup_field = 'username'

    def get_date_joined(self, obj):
        return naturaltime(obj.date_joined)


class UserListSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio')
    avatar = serializers.URLField(source='profile.avatar')
    status = serializers.URLField(source='profile.status')
    name = serializers.CharField(source='profile.name')


    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'bio',
            'avatar',
            'status',
            'is_staff',
            'date_joined'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', allow_blank=True)
    name = serializers.CharField(
    	source='profile.name',
    	max_length=32,
    	allow_blank=True
    )
    avatar = serializers.URLField(source='profile.avatar', allow_blank=True)
    status = serializers.CharField(
        source='profile.status',
    	allow_blank=True,
        default='',
        min_length=0,
    	max_length=16
    )
    current_password = serializers.CharField(
        write_only=True,
        allow_blank=True,
        label=_("Current Password"),
        help_text=_('Required'),
    )
    new_password = serializers.CharField(
        allow_blank=True,
        default='',
        write_only=True,
        min_length=4,
        max_length=32,
        label=_("New Password"),
    )
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
            'current_password',
            'new_password',
            'bio',
            'avatar',
            'status'
        )
        read_only_fields = ('username',)
        lookup_field = 'username'

    def update(self, instance, validated_data):
        try:
            username = self.context.get('request').user.username
        except:
            msg = _('Must be authenticated')
            raise serializers.ValidationError(msg, code='authorization')

        password = validated_data.get('current_password')
        validated_data.pop('current_password', None)

        if not password:
            msg = _('Must provide current password')
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(request=self.context.get('request'),
                            username=username, password=password)
        if not user:
            msg = _('Sorry, the password you entered is incorrect.')
            raise serializers.ValidationError(msg, code='authorization')


        new_password = validated_data.get('new_password') or None
        if new_password:
            instance.set_password(new_password)
        validated_data.pop('new_password', None)


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


# class UserCreateSerializer(serializers.ModelSerializer):
#     username = serializers.SlugField(
#         min_length=4,
#         max_length=32,
#         help_text=_(
#             'Required. 4-32 characters. Letters, numbers, underscores or hyphens only.'
#         ),
#         validators=[UniqueValidator(
#             queryset=User.objects.all(),
#             message='has already been taken by other user'
#         )],
#         required=True
#     )
#     password = serializers.CharField(
#         min_length=4,
#         max_length=32,
#         write_only=True,
#         help_text=_(
#             'Required. 4-32 characters.'
#         ),
#         required=True
#     )
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(
#             queryset=User.objects.all(),
#             message='has already been taken by other user'
#         )]
#     )
#     bio = serializers.CharField(source='profile.bio', allow_blank=True, default='')
#     name = serializers.CharField(
#         source='profile.name',
#         allow_blank=True,
#         default='',
#         max_length=32
#     )
#     avatar = serializers.URLField(source='profile.avatar', allow_blank=True, default='')
#     status = serializers.CharField(
#     	source='profile.status',
#     	allow_blank=True,
#     	max_length=16,
#         min_length=0,
#         default=''
#     )
#
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'name',
#             'email',
#             'password',
#             'bio',
#             'avatar',
#             'status'
#         )
#
#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile', None)
#         username = validated_data['username']
#         email = validated_data['email']
#         password = validated_data['password']
#         user = User(
#                 username = username,
#                 email = email
#         )
#         user.set_password(password)
#         user.save()
#
#         avatar = profile_data.get('avatar') or None
#         if not avatar:
#             avatar = 'https://api.adorable.io/avatar/200/' + username
#         profile = UserProfile(
#             user = user,
#             bio = profile_data.get('bio', ''),
#             avatar = avatar,
#             name = profile_data.get('name', ''),
#             status = profile_data.get('status', 'Member')
#         )
#         profile.save()
#         return user


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

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'password',
            'token',
        ]
        extra_kwargs = {"password": {"write_only": True} }


# TOPIC

class PostListSerializer(serializers.ModelSerializer):
    thread = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='thread-detail'
    )
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(allow_blank=False)
    thread = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='thread-detail'
    )
    thread_id = serializers.IntegerField(
        required=True,
        help_text=_('Required. Id of the thread this post is created in')
    )
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = "__all__"
        read_only_fields=('id', 'title', 'creator', 'content', 'moderator', 'status', 'slug',)

    def create(self, validated_data):
        content = validated_data['content']
        title = validated_data['title']
        moderator = validated_data['moderator']
        status = validated_data['status']
        slug = validated_data['slug']
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        else:
            raise serializers.ValidationError('Must be authenticated to create post')

        # Create the topic
        post = Topic(
            title=title,
            creator=user,
            moderator=moderator,
            content=content,
            status=status,
            slug=slug
        )
        # Update the thread last_activity to post creation time
        post.save()
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = "__all__"
        read_only_fields=('id', 'title', 'creator', 'content', 'moderator', 'status', 'slug',)

    def update(self, instance, validated_data):
        # Update fields if there is any change
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # Update 'updated_at' field to now
        setattr(instance, 'updated_at', now())

        # Note: If user update post, it won't change the last_activity
        instance.save()
        return instance


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    thread = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='thread-detail'
    )
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = '__all__'