# Generated by Django 3.0.2 on 2020-01-17 00:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200117_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='docker_container_path',
        ),
        migrations.AddField(
            model_name='submission',
            name='container_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='container_path',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='port',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 17, 0, 42, 29, 459593, tzinfo=utc)),
        ),
    ]
