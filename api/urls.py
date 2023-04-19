from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PostListView, DetailPostView, PostUpdateView, DeleteView, PostCreateView

urlpatterns = [
    path('login/', obtain_auth_token,name='obtain_auth_token'),
    path('list_post', PostListView.as_view(), name='post_view_api'),
    path('list_post/<int:pk>', DetailPostView.as_view(), name='post_detail_view_api'),
    path('list_post/update/<int:pk>', PostUpdateView.as_view(), name='post_update_view_api'),
    path('list_post/delete/<int:pk>', DeleteView.as_view(), name='post_delete_view_api'),
    path('list_post/create', PostCreateView.as_view(), name='post_create_view_api'),

]
# "token": "fc636533600fcc6aa7c8454b437745d9744e5f60"