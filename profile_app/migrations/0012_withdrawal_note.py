# Generated by Django 3.2.7 on 2021-10-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_app', '0011_withdrawal'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='note',
            field=models.CharField(default='', max_length=300),
        ),
    ]
