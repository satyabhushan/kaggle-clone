# Generated by Django 3.0.2 on 2020-01-16 19:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200117_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2012, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='competition',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 16, 19, 35, 7, 716693, tzinfo=utc)),
        ),
    ]