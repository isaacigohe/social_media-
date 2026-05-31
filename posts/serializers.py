from rest_framework import serializers
from .models import Post, Comment, PostLike, CommentLike, Hashtag
from users.serializers import UserMinimalSerializer


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    likes_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'parent', 'likes_count', 'is_liked', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    author = UserMinimalSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    hashtag_names = serializers.ListField(
        child=serializers.CharField(max_length=100), write_only=True, required=False
    )
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'content', 'image', 'video',
            'hashtags', 'hashtag_names',
            'likes_count', 'comments_count', 'is_liked',
            'created_at', 'updated_at',
        )
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False

    def create(self, validated_data):
        hashtag_names = validated_data.pop('hashtag_names', [])
        post = Post.objects.create(**validated_data)
        self._set_hashtags(post, hashtag_names)
        return post

    def update(self, instance, validated_data):
        hashtag_names = validated_data.pop('hashtag_names', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if hashtag_names is not None:
            self._set_hashtags(instance, hashtag_names)
        return instance

    def _set_hashtags(self, post, names):
        tags = []
        for name in names:
            name = name.lstrip('#').lower()
            tag, _ = Hashtag.objects.get_or_create(name=name)
            tags.append(tag)
        post.hashtags.set(tags)
