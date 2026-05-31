from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.me, name='me'),
    # Profiles
    path('profiles/<int:user_id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    # Follow
    path('users/<int:user_id>/follow/', views.follow_user, name='follow-user'),
    # Search
    path('search/users/', views.search_users, name='search-users'),
    # Notifications
    path('notifications/', views.notifications_list, name='notifications'),
]
