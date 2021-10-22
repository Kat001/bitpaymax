# Generated by Django 3.2.7 on 2021-10-18 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_auto_20210930_1838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(default='', max_length=40)),
                ('account_number', models.CharField(default='', max_length=30)),
                ('branch_name', models.CharField(default='', max_length=40)),
                ('ifsc_code', models.CharField(default='', max_length=20)),
                ('bank_name', models.CharField(default='', max_length=30)),
                ('nominee_name', models.CharField(default='', max_length=30)),
                ('cheak', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]