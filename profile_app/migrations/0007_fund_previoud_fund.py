# Generated by Django 3.2.7 on 2021-09-24 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0006_fundrecord_fundtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='previoud_fund',
            field=models.PositiveIntegerField(default=0),
        ),
    ]