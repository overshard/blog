# Generated by Django 4.0.5 on 2022-06-12 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_searchpage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpostpage',
            options={'ordering': ['-first_published_at'], 'verbose_name': 'Blog Post Page', 'verbose_name_plural': 'Blog Post Pages'},
        ),
    ]
