from rest_framework import serializers

from accounts.models import Profile
from .models import Draw


class DrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draw
        fields = [
            'id', 'title', 'description', 'is_published',
            'author', 'liked_ids', 'like_count'
        ]

    author = serializers.StringRelatedField()
    liked_ids = serializers.PrimaryKeyRelatedField(
        source='like',
        queryset=Profile.objects.all(),
        many=True,
    )
