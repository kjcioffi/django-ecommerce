# Generated by Django 5.0.6 on 2024-07-10 14:45

import store.store_utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_store_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, upload_to=store.store_utils.StoreUtils.generate_store_image_path),
        ),
    ]
