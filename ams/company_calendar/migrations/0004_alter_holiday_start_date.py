# Generated by Django 4.0.3 on 2022-04-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_calendar', '0003_alter_holiday_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='start_date',
            field=models.DateField(),
        ),
    ]