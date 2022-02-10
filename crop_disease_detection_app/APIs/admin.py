from django.contrib import admin
from .models import *
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import SafeText

admin.site.site_header = "Crop Disease Detection Admin Dashboard"

def model_admin_url(obj, name=None) -> str:
    url = resolve_url(admin_urlname(obj._meta, SafeText("change")), obj.pk)
    return format_html('<a href="{}">{}</a>', url, name or str(obj))

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("user_name", "email", "password")
    search_fields = ("user_name", "email")
    ordering = ("user_name", "email")

@admin.register(Data)
class Data(admin.ModelAdmin):
    list_display = ("time_stamp", "latitude", "longitude", "predicted_class", "probability", "user", "crop_type", "image")
    search_fields = ("user", "crop_type", "predicted_class")
    ordering = ("time_stamp", "user", "crop_type")

@admin.register(Crop)
class Crop(admin.ModelAdmin):
    list_display = ("crop_name", "crop_desc")
    search_fields = ("crop_name", "crop_desc")
    ordering = ("crop_name", "crop_desc")

@admin.register(Developer)
class Developer(admin.ModelAdmin):
    list_display = ("dev_name", "email")
    search_fields = ("dev_name", "email")
    ordering = ("dev_name", "email")

