# Generated by Django 3.2.10 on 2022-04-08 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0015_auto_20220408_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictedclass',
            name='predicted_class',
            field=models.CharField(choices=[('northern_leaf_blight', 'northern_leaf_blight'), ('cercospora_gray_leaf_spot', 'cercospora_gray_leaf_spot'), ('common_rust', 'common_rust'), ('healthy', 'healthy'), ('nutrient_deficient', 'nutrient_deficient'), ('disease1_cotton', 'disease1_cotton'), ('disease2_cotton', 'disease2_cotton'), ('disease3_cotton', 'disease3_cotton'), ('disease4_cotton', 'disease4_cotton'), ('disease5_cotton', 'disease5_cotton'), ('disease1_rice', 'disease1_rice'), ('disease2_rice', 'disease2_rice'), ('disease3_rice', 'disease3_rice'), ('disease4_rice', 'disease4_rice'), ('disease5_rice', 'disease5_rice'), ('disease1_wheat', 'disease1_wheat'), ('disease2_wheat', 'disease2_wheat'), ('disease3_wheat', 'disease3_wheat'), ('disease4_wheat', 'disease4_wheat'), ('disease5_wheat', 'disease5_wheat'), ('disease1_jute', 'disease1_jute'), ('disease2_jute', 'disease2_jute'), ('disease3_jute', 'disease3_jute'), ('disease4_jute', 'disease4_jute'), ('disease5_jute', 'disease5_jute')], max_length=100, primary_key=True, serialize=False),
        ),
    ]
