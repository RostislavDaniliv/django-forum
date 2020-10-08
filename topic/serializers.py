from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from .models import Topic
from comments.serializers import CommentSerializer


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
        post = Topic(
            title=title,
            creator=user,
            moderator=moderator,
            content=content,
            status=status,
            slug=slug
        )
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
        for field, value in validated_data.items():
            setattr(instance, field, value)
        setattr(instance, 'updated_at', now())
        instance.save()
        return instance


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class PostDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    reviews = CommentSerializer(many=True)
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


class SetModerInTopicSerializer(serializers.ModelSerializer):
    moderator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = ['moderator']
        read_only_fields=('moderator',)
        lookup_field = 'username'

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        setattr(instance, 'updated_at', now())
        instance.save()
        return instance

