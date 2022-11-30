# Generated by Django 4.1.3 on 2022-11-30 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Título')),
                ('description', models.CharField(max_length=140, verbose_name='Descrição')),
                ('slug', models.SlugField(unique=True)),
                ('about', models.TextField(verbose_name='Sobre')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('img', models.ImageField(blank=True, default=None, upload_to='draws/cover/%Y/%m/%d/', verbose_name='Desenho')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publicado')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
    ]
