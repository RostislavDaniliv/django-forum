# Generated by Django 3.1.1 on 2020-10-07 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_bans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_ban',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_mute',
        ),
    ]
