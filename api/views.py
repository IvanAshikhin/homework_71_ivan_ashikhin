from django.shortcuts import get_object_or_404
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permission import IsAuthor
from api.serializes import PostSerializer
from posts.models import Post


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        objects = Post.objects.all()
        serializer = PostSerializer(objects, many=True)
        return Response(serializer.data)


class DetailPostView(APIView):
    def get(self, request, pk):
        objects = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(objects)
        return Response(serializer.data)


class DeleteView(APIView):
    permission_classes = [IsAuthor]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_pk = post.pk
        post.delete()
        data = {'post_pk': post_pk}
        return Response(data)


class PostUpdateView(APIView):
    permission_classes = [IsAuthor]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.user_likes.all():
            post.likes_count -= 1
            post.user_likes.remove(user)
            post.save()
            return Response({'detail': 'Post unliked successfully.'})
        else:
            post.likes_count += 1
            post.user_likes.add(user)
            post.save()
            return Response({'detail': 'Post liked successfully.'})
