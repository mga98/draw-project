# Generated by Django 4.1.4 on 2022-12-20 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_img',
            field=models.ImageField(blank=True, default='', upload_to='accounts/cover/%Y/%m/%d/', verbose_name='Desenho'),
        ),
    ]