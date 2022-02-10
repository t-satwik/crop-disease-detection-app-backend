# Generated by Django 3.2.10 on 2022-02-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0009_videoframe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='predicted_class',
            field=models.TextField(choices=[('northern_leaf_blight', 'northern_leaf_blight'), ('cercospora_gray_leaf_spot', 'cercospora_gray_leaf_spot'), ('common_rust', 'common_rust'), ('healthy', 'healthy'), ('nutrient_deficient', 'nutrient_deficient')], max_length=100),
        ),
    ]
