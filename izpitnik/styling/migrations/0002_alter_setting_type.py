# Generated by Django 5.1.2 on 2024-11-15 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('styling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='type',
            field=models.CharField(blank=True, choices=[], max_length=15),
        ),
    ]
