# Generated by Django 4.0.3 on 2022-03-31 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('day', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
    ]
