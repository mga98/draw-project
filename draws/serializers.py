from rest_framework import serializers

from accounts.models import Profile


class DrawSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=35)
    description = serializers.CharField(max_length=40)
    is_published = serializers.BooleanField()
    author = serializers.StringRelatedField()
    liked_ids = serializers.PrimaryKeyRelatedField(
        source='like',
        queryset=Profile.objects.all(),
        many=True,
    )
    like_count = serializers.IntegerField()

    def profile_method(self, profile):
        user = profile.objects.all()
        return user.likes()
