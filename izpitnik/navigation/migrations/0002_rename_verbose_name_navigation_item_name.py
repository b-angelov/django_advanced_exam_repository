# Generated by Django 5.1.2 on 2024-11-14 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='navigation',
            old_name='verbose_name',
            new_name='item_name',
        ),
    ]
