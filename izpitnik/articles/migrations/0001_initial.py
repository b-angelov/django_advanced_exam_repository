# Generated by Django 5.1.2 on 2024-12-05 22:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orth_calendar', '0008_alter_holidayoccurrences_feast_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('content', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('feast', models.ManyToManyField(blank=True, to='orth_calendar.feast')),
                ('holiday', models.ManyToManyField(blank=True, to='orth_calendar.holidayoccurrences')),
                ('saint', models.ManyToManyField(blank=True, to='orth_calendar.saint')),
            ],
        ),
    ]