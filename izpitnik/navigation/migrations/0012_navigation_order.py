# Generated by Django 5.1.2 on 2024-11-24 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0011_alter_menu_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigation',
            name='order',
            field=models.SmallIntegerField(blank=True, default=0),
        ),
    ]
