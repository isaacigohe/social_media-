from django.contrib import admin
from .models import Post, Comment, PostLike, CommentLike, Hashtag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'likes_count', 'comments_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'likes_count', 'created_at')

admin.site.register(Hashtag)
admin.site.register(PostLike)
admin.site.register(CommentLike)
