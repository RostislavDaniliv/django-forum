from rest_framework import serializers
from django.utils.timezone import now
from .models import Comment, Topic


class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=False)
    text = serializers.CharField(allow_blank=False)
    parent = serializers.HyperlinkedRelatedField(read_only=True,
        view_name='CommentDetail',
        lookup_field='comment_id')
    topic = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='TopicDetail',
        lookup_field='topic_id'
    )

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        name = validated_data['name']
        text = validated_data['text']
        topic = None
        parent = None
        request = self.context.get("request")
        if request and hasattr(request, "parent"):
            parent = request.comment
        if request and hasattr(request, "topic"):
            topic = request.topic
        comm = Comment(
            name=name,
            text=text,
            parent=parent,
            topic=topic,
        )
        comm.save()
        return comm


class FilterCommentsListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentsListSerializer
        model = Comment
        fields = ("id", "name", "text", "children")


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    creator = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = Topic
        fields = "__all__"

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        setattr(instance, 'updated_at', now())

        instance.save()
        return instance