# Generated by Django 3.2.7 on 2021-10-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210923_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_able_for_income',
            field=models.BooleanField(default=False),
        ),
    ]
