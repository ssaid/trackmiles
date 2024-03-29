# Generated by Django 4.1.4 on 2023-05-28 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='airport',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='airports', to='flights.country'),
        ),
        migrations.AlterField(
            model_name='airport',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='airports', to='flights.region'),
        ),
        migrations.AlterField(
            model_name='suscriptions',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suscriptions', to='flights.product'),
        ),
        migrations.AlterField(
            model_name='suscriptions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suscriptions', to=settings.AUTH_USER_MODEL),
        ),
    ]
