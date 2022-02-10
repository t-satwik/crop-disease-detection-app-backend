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

def upload_to(instance, folder_path):
    time_stamp=instance.time_stamp
    time_stamp=time_stamp.replace('/', '-')
    time_stamp=time_stamp.replace(' ', '_')
    time_stamp=time_stamp.replace(':', '-')
    user_name=instance.user_name
    user_name=user_name.replace('/', '-')
    user_name=user_name.replace(' ', '_')
    user_name=user_name.replace(':', '-')
    crop_type=instance.user_name
    crop_type=crop_type.replace('/', '-')
    crop_type=crop_type.replace(' ', '_')
    crop_type=crop_type.replace(':', '-')
    file_name=user_name+'_'+crop_type+"_"+time_stamp+'.png'
    return folder_path+file_name

class Data(models.Model):
    time_stamp = models.TextField(null=False)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=False)
    predicted_class=models.TextField(blank=False)
    probability = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
    user=models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=True)
    crop_type=models.ForeignKey(Crop, blank=False, on_delete=models.CASCADE, null=True)
    # image_path=upload_to(folder_path='media/')
    # image_path=models.TextField(blank=False)
    # image=models.ImageField(_("IMAGE"), upload_to=image_path, default='images/default.png')
    

# class VideoFrame(models.Model):
#     time_stamp = models.TextField(null=False)
#     startLatitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
#     startLongitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
#     endLatitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
#     endLongitude = models.DecimalField(max_digits=22, decimal_places=16, blank=False, null=False)
#     user=models.ForeignKey(User, blank=False, on_delete=models.CASCADE, null=False)
#     predicted_class=models.TextField(null=False)
#     crop_type=models.ForeignKey(Crop, blank=False, on_delete=models.CASCADE)
#     probability = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
#     # image_path=upload_to(folder_path='videoframes/')
#     image_path=models.TextField(blank=False)
#     image=models.ImageField(_("IMAGE"), upload_to=image_path, default='videoframes/default.png')
    
class Developer(models.Model):
    dev_name = models.CharField(blank=False, primary_key=True, max_length=100, default="default_name")
    password = models.CharField(blank=True, null=True, max_length=150)
    email = models.CharField(blank=False, null=True, max_length=100)    