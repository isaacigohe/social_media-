from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer
from users.models import Notification


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # News feed: posts from followed users + own posts
        user = self.request.user
        following_ids = user.following.values_list('following_id', flat=True)
        return Post.objects.filter(
            Q(author__in=following_ids) | Q(author=user)
        ).select_related('author').prefetch_related('hashtags', 'likes')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all().select_related('author').prefetch_related('hashtags')
    lookup_url_kwarg = 'post_id'

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'detail': 'You can only edit your own posts.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'detail': 'You can only delete your own posts.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id, parent=None).select_related('author').prefetch_related('replies')

    def perform_create(self, serializer):
        post = generics.get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = serializer.save(author=self.request.user, post=post)
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=self.request.user,
                notification_type='comment',
                post=post,
                comment=comment,
            )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'comment_id'

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({'detail': 'You can only edit your own comments.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({'detail': 'You can only delete your own comments.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = generics.get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like_post',
                post=post,
            )
        return Response({'detail': 'Post liked.', 'likes_count': post.likes_count}, status=status.HTTP_201_CREATED)
    else:
        deleted, _ = PostLike.objects.filter(user=request.user, post=post).delete()
        if not deleted:
            return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Like removed.', 'likes_count': post.likes_count})


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def like_comment(request, comment_id):
    comment = generics.get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        if comment.author != request.user:
            Notification.objects.create(
                recipient=comment.author,
                sender=request.user,
                notification_type='like_comment',
                comment=comment,
            )
        return Response({'detail': 'Comment liked.', 'likes_count': comment.likes_count}, status=status.HTTP_201_CREATED)
    else:
        deleted, _ = CommentLike.objects.filter(user=request.user, comment=comment).delete()
        if not deleted:
            return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Like removed.', 'likes_count': comment.likes_count})
