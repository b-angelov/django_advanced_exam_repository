# Generated by Django 5.1.2 on 2024-11-23 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0006_alter_navigation_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigation',
            name='language',
            field=models.CharField(choices=[('en-US', 'English'), ('bg-BG', 'Bulgarian')], default='en', max_length=7),
        ),
    ]
