# Generated by Django 3.0.5 on 2020-08-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20200822_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='room_desc',
            field=models.CharField(max_length=200),
        ),
    ]
