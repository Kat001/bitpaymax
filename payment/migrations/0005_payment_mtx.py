# Generated by Django 3.2.7 on 2021-10-24 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_bank_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='mtx',
            field=models.CharField(default='', max_length=200),
        ),
    ]