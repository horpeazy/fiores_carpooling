# Generated by Django 3.2.16 on 2023-02-28 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpooling', '0009_trip_requests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_trip', to='carpooling.trip'),
        ),
    ]
