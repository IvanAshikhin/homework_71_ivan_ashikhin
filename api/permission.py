from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from posts.models import Post


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in ['PUT', 'DELETE']:
            post = get_object_or_404(Post, pk=view.kwargs['pk'])
            return post.author == user
        else:
            return True

