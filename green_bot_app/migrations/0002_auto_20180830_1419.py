# Generated by Django 2.1 on 2018-08-30 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('green_bot_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoorUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_door_time', models.DateTimeField(verbose_name='request_for_door')),
                ('opened_door_time', models.DateTimeField(blank=True, default=None, verbose_name='success_request')),
            ],
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='can_open_door',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='doorusage',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='green_bot_app.TelegramUser'),
        ),
    ]
