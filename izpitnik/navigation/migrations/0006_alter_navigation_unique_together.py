# Generated by Django 5.1.2 on 2024-11-23 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0005_navigation_language'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='navigation',
            unique_together={('slug', 'url_external', 'url_internal', 'language')},
        ),
    ]