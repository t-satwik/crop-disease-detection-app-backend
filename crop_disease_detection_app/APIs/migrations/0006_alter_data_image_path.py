# Generated by Django 3.2.10 on 2022-02-10 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0005_alter_data_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='image_path',
            field=models.TextField(blank=True, default='default_path', null=True),
        ),
    ]
