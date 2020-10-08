from rest_framework import serializers
from django.utils.timezone import now
from .models import Comment, Topic


class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


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