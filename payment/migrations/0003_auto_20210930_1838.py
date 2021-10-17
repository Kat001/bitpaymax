# Generated by Django 3.2.7 on 2021-09-30 18:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='btcAmount',
            new_name='cryptoPayment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='ethAmount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='inrAmount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='trxAmount',
        ),
        migrations.AddField(
            model_name='payment',
            name='createdOn',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
