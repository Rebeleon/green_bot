# Generated by Django 2.1 on 2018-09-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_bot_app', '0003_auto_20180903_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doorusage',
            name='opened_door_time',
        ),
        migrations.AddField(
            model_name='doorusage',
            name='opened_door',
            field=models.BooleanField(default=False, verbose_name='success_request'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='opened_door_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]