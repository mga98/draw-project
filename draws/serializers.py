from rest_framework import serializers


class DrawSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=35)
    description = serializers.CharField(max_length=40)
