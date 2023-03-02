from rest_framework import serializers

from accounts.validators import DrawValidator
from .models import Draw


class DrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draw
        fields = [
            'id', 'title', 'description', 'is_published',
            'author', 'about'
        ]

    author = serializers.StringRelatedField()

    def validate(self, attrs):
        if self.instance is not None and attrs.get('title') is None:
            attrs['title'] = self.instance.title

        if self.instance is not None and attrs.get('about') is None:
            attrs['about'] = self.instance.about

        super_validate = super().validate(attrs)
        DrawValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )

        return super_validate
