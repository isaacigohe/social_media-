from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Follow, Notification
from .serializers import (
    RegisterSerializer, ProfileSerializer, ProfileUpdateSerializer,
    NotificationSerializer, UserMinimalSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return generics.get_object_or_404(User, pk=user_id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({'detail': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    target = generics.get_object_or_404(User, pk=user_id)
    if target == request.user:
        return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        return Response({'detail': 'Already following.'}, status=status.HTTP_400_BAD_REQUEST)
    Notification.objects.create(
        recipient=target, sender=request.user, notification_type='follow'
    )
    return Response({'detail': f'Now following {target.username}.'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    target = generics.get_object_or_404(User, pk=user_id)
    deleted, _ = Follow.objects.filter(follower=request.user, following=target).delete()
    if not deleted:
        return Response({'detail': 'Not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': f'Unfollowed {target.username}.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    query = request.query_params.get('query', '').strip()
    if not query:
        return Response({'detail': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    users = User.objects.filter(username__icontains=query) | User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)
    users = users.exclude(pk=request.user.pk).distinct()[:20]
    serializer = ProfileSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related('sender')[:50]
    serializer = NotificationSerializer(notifications, many=True)
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    serializer = ProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data)
