# Generated by Django 5.1.2 on 2024-11-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Navigation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('verbose_name', models.CharField(max_length=50)),
                ('url_external', models.URLField(blank=True, null=True)),
                ('url_internal', models.SlugField(blank=True, null=True)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=models.SET(-1), related_name='children', to='navigation.navigation')),
            ],
            options={
                'unique_together': {('slug', 'url_external', 'url_internal')},
            },
        ),
    ]