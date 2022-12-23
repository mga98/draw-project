import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from accounts.models import Profile


class Draw(models.Model):
    title = models.CharField('Título', max_length=35)
    description = models.CharField('Descrição', max_length=40)
    slug = models.SlugField(unique=True)
    about = models.TextField('Sobre')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    author = models.ForeignKey(
        User, verbose_name='Usuário', on_delete=models.SET_NULL, null=True
    )
    img = models.ImageField(
        'Desenho', upload_to='draws/cover/%Y/%m/%d/', blank=True, default=''
    )
    is_published = models.BooleanField('Publicado', default=False)
    like = models.ManyToManyField(
        Profile, related_name='like', default=None, blank=True
    )
    like_count = models.BigIntegerField(default='0')

    def __str__(self):
        return self.title

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

        if self.img:
            try:
                self.resize_image(self.img, 1920)

            except FileNotFoundError:
                ...

        return saved


class DrawComment(models.Model):
    draw = models.ForeignKey(
        Draw, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment_user', null=True, default=''  # noqa
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
