# Generated by Django 5.1.5 on 2025-02-16 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_bookmodel_likes_bookmodel_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
