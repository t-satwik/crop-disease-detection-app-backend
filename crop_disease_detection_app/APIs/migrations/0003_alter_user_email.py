# Generated by Django 3.2.10 on 2022-02-10 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0002_alter_crop_crop_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=150, null=True),
        ),
    ]