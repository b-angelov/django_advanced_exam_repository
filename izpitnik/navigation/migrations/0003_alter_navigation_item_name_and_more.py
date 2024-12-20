# Generated by Django 5.1.2 on 2024-11-23 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0002_rename_verbose_name_navigation_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigation',
            name='item_name',
            field=models.CharField(max_length=50, verbose_name='item name'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(-1), related_name='children', to='navigation.navigation', verbose_name='parent ID'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='url_external',
            field=models.URLField(blank=True, null=True, verbose_name='external URL'),
        ),
        migrations.AlterField(
            model_name='navigation',
            name='url_internal',
            field=models.SlugField(blank=True, null=True, verbose_name='internal URL'),
        ),
    ]
