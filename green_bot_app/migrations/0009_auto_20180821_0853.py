# Generated by Django 2.1 on 2018-08-21 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('green_bot_app', '0008_delete_vote'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserTelegramBot',
            new_name='Organisation',
        ),
    ]
