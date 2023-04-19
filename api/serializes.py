from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('created_at', 'comments_count', 'likes_count', 'description', 'image', 'author')
