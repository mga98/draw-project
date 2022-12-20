import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    user_img = models.ImageField(
        'Imagem de usuário',
        upload_to='accounts/cover/%Y/%m/%d/',
        blank=True, default=''
    )

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()

            return

        new_height = round((new_width * original_height) / original_width)
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)

        if self.user_img:
            try:
                self.resize_image(self.user_img, 1920)

            except FileNotFoundError:
                ...

        return saved
