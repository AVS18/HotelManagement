# Generated by Django 3.0.5 on 2020-08-22 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.BigIntegerField(null=True),
        ),
    ]
