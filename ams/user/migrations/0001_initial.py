# Generated by Django 4.0.3 on 2022-03-31 05:40

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('shift_start', models.TimeField()),
                ('shift_end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('role', models.TextField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('password', models.CharField(max_length=256)),
                ('device_id', models.BigIntegerField(unique=True)),
                ('is_active', models.BooleanField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.departments')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.roles')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
