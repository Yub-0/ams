# Generated by Django 4.0.3 on 2022-04-22 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_calendar', '0002_rename_day_holiday_end_date_holiday_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='start_date',
            field=models.DateField(unique=True),
        ),
    ]