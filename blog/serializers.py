from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'created_at', 'updated_at', 'is_approved']


class CommentValidateSerializer(serializers.Serializer):
    body = serializers.CharField(min_length=1)
    is_approved = serializers.BooleanField(default=True)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'created_at', 'updated_at', 'is_published']


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'body', 'created_at', 'updated_at', 'is_published', 'comments']


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=2)
    body = serializers.CharField()
    is_published = serializers.BooleanField(default=True)