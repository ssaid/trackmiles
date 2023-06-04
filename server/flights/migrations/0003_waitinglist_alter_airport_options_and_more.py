# Generated by Django 4.1.4 on 2023-06-04 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_product_active_alter_airport_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='airport',
            options={'ordering': ['country__name', 'name']},
        ),
        migrations.AlterField(
            model_name='preference',
            name='airport_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_destination', to='flights.airport'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='airport_origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_origin', to='flights.airport'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='country_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_destination', to='flights.country'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='country_origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_origin', to='flights.country'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='region_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_destination', to='flights.region'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='region_origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_origin', to='flights.region'),
        ),
    ]
