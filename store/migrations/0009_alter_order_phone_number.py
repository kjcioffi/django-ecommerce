# Generated by Django 5.0.1 on 2024-02-01 17:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(validators=[django.core.validators.RegexValidator('^\\d{3}-\\d{3}-\\d{4}$')]),
        ),
    ]