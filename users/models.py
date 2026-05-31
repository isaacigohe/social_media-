from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website = models.URLField(blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def posts_count(self):
        return self.posts.count()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table = 'follows'

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like_post', 'Liked your post'),
        ('like_comment', 'Liked your comment'),
        ('comment', 'Commented on your post'),
        ('follow', 'Started following you'),
        ('mention', 'Mentioned you'),
    ]

    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey('posts.Post', null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('posts.Comment', null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.sender} → {self.recipient}: {self.notification_type}'
