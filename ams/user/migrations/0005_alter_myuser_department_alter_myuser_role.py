# Generated by Django 4.0.3 on 2022-04-07 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_myuser_department_alter_myuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='department',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='user.department'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='user.role'),
        ),
    ]
