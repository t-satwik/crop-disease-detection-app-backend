# Generated by Django 3.2.10 on 2022-02-10 08:16

import APIs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0006_alter_data_image_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='image',
            field=models.ImageField(default='images/default.png', upload_to=APIs.models.upload_to, verbose_name='IMAGE'),
        ),
    ]
