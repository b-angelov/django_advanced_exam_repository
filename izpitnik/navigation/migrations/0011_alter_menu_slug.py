# Generated by Django 5.1.2 on 2024-11-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0010_alter_navigation_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='slug'),
        ),
    ]