# Generated by Django 4.1.3 on 2022-12-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('draws', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draw',
            name='img',
            field=models.ImageField(blank=True, default='', upload_to='draws/cover/%Y/%m/%d/', verbose_name='Desenho'),
        ),
    ]