# Generated by Django 5.0.6 on 2024-07-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_order_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
