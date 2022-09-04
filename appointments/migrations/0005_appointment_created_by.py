# Generated by Django 4.0.6 on 2022-08-23 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0004_alter_appointment_canceled_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='created_by',
            field=models.ForeignKey(default=26, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]