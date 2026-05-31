from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/like/', views.like_post, name='like-post'),
    path('comments/<int:comment_id>/like/', views.like_comment, name='like-comment'),
]
