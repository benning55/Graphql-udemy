# Generated by Django 3.1 on 2020-08-31 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200831_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.director'),
        ),
    ]
