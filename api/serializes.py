from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'created_at', 'comments_count', 'likes_count', 'description', 'image', 'author')
        read_only_fields = ('id', 'created_at', 'likes_count', 'comments_count')
