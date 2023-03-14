# Generated by Django 3.2.16 on 2023-03-13 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpooling', '0016_auto_20230312_0446'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='trip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='carpooling.trip'),
            preserve_default=False,
        ),
    ]
