# Generated by Django 4.0.5 on 2022-06-16 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledtask',
            name='next_run_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
