# Generated by Django 4.0.3 on 2022-04-06 06:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DailyLogs',
            new_name='DailyLog',
        ),
    ]