# Generated by Django 3.0.2 on 2020-01-16 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200117_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='competition',
        ),
        migrations.DeleteModel(
            name='Competition',
        ),
        migrations.DeleteModel(
            name='Submission',
        ),
    ]
