# Generated by Django 5.1.2 on 2024-11-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orth_calendar', '0007_relatedholidayoccurrences_alter_feast_saint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holidayoccurrences',
            name='feast',
            field=models.ManyToManyField(blank=True, default=None, related_name='occurrences', to='orth_calendar.feast', verbose_name='feast'),
        ),
        migrations.AlterField(
            model_name='holidayoccurrences',
            name='saint',
            field=models.ManyToManyField(blank=True, default=None, related_name='occurrences', to='orth_calendar.saint', verbose_name='saint'),
        ),
    ]
