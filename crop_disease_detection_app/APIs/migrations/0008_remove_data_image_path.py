# Generated by Django 3.2.10 on 2022-02-10 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0007_alter_data_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='image_path',
        ),
    ]
