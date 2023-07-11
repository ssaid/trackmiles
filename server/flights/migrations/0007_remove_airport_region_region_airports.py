# Generated by Django 4.1.4 on 2023-07-11 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_alter_flighthistory_options_flighthistory_fare_clean_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airport',
            name='region',
        ),
        migrations.AddField(
            model_name='region',
            name='airports',
            field=models.ManyToManyField(to='flights.airport'),
        ),
    ]