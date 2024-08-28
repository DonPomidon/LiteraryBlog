# Generated by Django 5.0.7 on 2024-08-23 07:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_review_rating_only'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('book', 'user', 'rating')},
        ),
    ]
