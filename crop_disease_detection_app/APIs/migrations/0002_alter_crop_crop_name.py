# Generated by Django 3.2.10 on 2022-02-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='crop_name',
            field=models.CharField(choices=[('maize', 'maize'), ('cotton', 'cotton'), ('rice', 'rice')], max_length=100, primary_key=True, serialize=False),
        ),
    ]