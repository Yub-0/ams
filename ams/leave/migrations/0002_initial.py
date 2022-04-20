# Generated by Django 4.0.3 on 2022-04-20 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffleave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='staffleave',
            unique_together={('date', 'user')},
        ),
    ]
