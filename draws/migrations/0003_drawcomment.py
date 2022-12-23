# Generated by Django 4.1.4 on 2022-12-22 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('draws', '0002_alter_draw_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=15)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('draw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='draws.draw')),
            ],
        ),
    ]