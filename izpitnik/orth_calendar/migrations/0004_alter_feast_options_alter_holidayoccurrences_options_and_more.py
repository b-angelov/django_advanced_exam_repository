# Generated by Django 5.1.2 on 2024-11-23 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orth_calendar', '0003_alter_holidayoccurrences_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feast',
            options={'verbose_name': 'feast'},
        ),
        migrations.AlterModelOptions(
            name='holidayoccurrences',
            options={'verbose_name': 'holiday occurrence', 'verbose_name_plural': 'holiday occurrences'},
        ),
        migrations.AlterModelOptions(
            name='saint',
            options={'verbose_name': 'saint'},
        ),
    ]
