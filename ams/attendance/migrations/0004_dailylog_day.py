# Generated by Django 4.0.3 on 2022-04-17 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_remove_dailylog_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailylog',
            name='day',
            field=models.DateTimeField(default=datetime.date(2022, 4, 17)),
        ),
    ]