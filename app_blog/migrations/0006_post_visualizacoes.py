# Generated by Django 5.2 on 2025-05-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0005_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visualizacoes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
