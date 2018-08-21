# Generated by Django 2.1 on 2018-08-20 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('green_bot_app', '0006_vote_message_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_telegram', models.IntegerField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('voted', models.BooleanField(default=False)),
            ],
        ),
    ]