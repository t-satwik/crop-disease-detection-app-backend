from django.db import models
from .utils import *
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(models.Model):
    user_name = models.CharField(blank=False, primary_key=True, max_length=100, default="default_name")
    password = models.CharField(blank=True, null=True, max_length=150)
    email = models.CharField(blank=False, null=True, max_length=150)


class Crop(models.Model):
    crop_name=models.CharField(blank=False, primary_key=True, choices=ALLOWED_CROP_TYPES, max_length=100)
    # crop_name=models.CharField(blank=False, primary_key=True, max_length=150, default="default_name")
    crop_desc=models.CharField(blank=False, null=False, max_length=300, default="default_desc")

class PredictedClass(models.Model):
    predicted_class=models.CharField(blank=False, primary_key=True, choices=ALLOWED_PREDICTED_CLASSES, max_length=100)
    class_desc=models.CharField(blank=False, null=False, max_length=300, default="default_desc")
    crop_type=models.ForeignKey(Crop, blank=False, on_delete=models.CASCADE, null=True)

def clean_str(var):
    var=var.replace('/', '-')
    var=var.replace(' ', '_')
    var=var.replace(':', '-')
    return var

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    ts=clean_str(instance.time_stamp)
    un=clean_str(instance.user.user_name)
    ct=clean_str(instance.crop_type.crop_name)
    filename=un+'_'+ct+"_"+ts+'.'+ext
    return 'images/{filename}'.format(filename=filename)

class Data(models.Model):
    time_stamp = models.TextField(null=False)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    predicted_class=models.ForeignKey(PredictedClass, blank=False, on_delete=models.CASCADE, null=True)
    probability = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    user=models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=True)
    crop_type=models.ForeignKey(Crop, blank=False, on_delete=models.CASCADE, null=True)
    image=models.ImageField(_("IMAGE"), upload_to=upload_to, default='images/default.png')
    
class VideoFrame(models.Model):
    time_stamp = models.TextField(null=False)
    start_latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    start_longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    end_latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    end_longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    predicted_class=models.ForeignKey(PredictedClass, blank=False, on_delete=models.CASCADE, null=True)
    probability = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    user=models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=True)
    crop_type=models.ForeignKey(Crop, blank=False, on_delete=models.CASCADE, null=True)
    frame=models.ImageField(_("IMAGE"), upload_to=upload_to, default='images/default.png')

class Sensor(models.Model):
    sensor_type = models.CharField(max_length=100, choices=ALLOWED_SENSOR_TYPES, default="temperature")
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

class SensorValue(models.Model):
    value=models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    sensor=models.ForeignKey(Sensor, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    time_stamp = models.TextField(null=False)
    sensor_type=models.CharField(max_length=100, choices=ALLOWED_SENSOR_TYPES, default="temperature")

class Developer(models.Model):
    dev_name = models.CharField(blank=False, primary_key=True, max_length=100, default="default_name")
    password = models.CharField(blank=True, null=True, max_length=150)
    email = models.CharField(blank=False, null=True, max_length=100)    