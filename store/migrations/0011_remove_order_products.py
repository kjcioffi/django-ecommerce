# Generated by Django 5.0.1 on 2024-02-09 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
