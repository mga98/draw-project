from rest_framework import serializers

from accounts.validators import DrawValidator
from .models import Draw


class DrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draw
        fields = [
            'id', 'title', 'description', 'is_published',
            'author', 'about', 'img'
        ]

    author = serializers.StringRelatedField()

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        DrawValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )

        return super_validate
