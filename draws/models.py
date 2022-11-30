from django.db import models
from django.contrib.auth.models import User


class Draw(models.Model):
    title = models.CharField('Título', max_length=40)
    description = models.CharField('Descrição', max_length=140)
    slug = models.SlugField(unique=True)
    about = models.TextField('Sobre')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    author = models.ForeignKey(
        User, verbose_name='Usuário', on_delete=models.SET_NULL, null=True
    )
    img = models.ImageField(
        'Desenho', upload_to='draws/cover/%Y/%m/%d/', blank=True, default=None
    )
    is_published = models.BooleanField('Publicado', default=False)

    def __str__(self):
        return self.title
