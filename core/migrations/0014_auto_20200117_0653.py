# Generated by Django 3.0.2 on 2020-01-17 01:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200117_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 17, 1, 23, 59, 87575, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='accuracy',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
