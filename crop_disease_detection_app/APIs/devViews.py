from .models import *
from django.shortcuts import get_object_or_404
import sys
import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages


def developerView(request):
    return render(request, 'developer/home.html')


def devLogin(request):
    #Use token mechanism here also
    if request.method=='POST':
        try:
            username=request.POST['username']
            password=(hashlib.md5(request.POST['pass'].encode('utf-8')).hexdigest())
            print(password)
            admin_obj = get_object_or_404(Developer, user_name=username)
            if admin_obj is not None:
                if(password == admin_obj.password):
                    messages.success(request, "Admin Verified")
                    return redirect('/apis/dev/home')
                else:
                    messages.success(request, "invalid credentials")
                    return redirect('/apis/dev/login')
            else:
                messages.success(request, "invalid credentials")
                return redirect('/apis/dev/login')
        except Exception:
            print(sys.exc_info())
            return redirect('/apis/dev/login')
    else:
        return render(request, 'developer/login.html')
    
def devHome(request):
    user_name=request.POST.get('username', False)
    predicted_class=request.POST.get('predicted_class', False)
    crop_type=request.POST.get('crop_type', False)
    latitude=float(request.POST.get('latitude', False))
    longitude=float(request.POST.get('longitude', False))
    offset=float(request.POST.get('offset', False))
    # print(user_name)
    if(user_name):
        print("user_name search")
        data=Data.objects.filter(user__exact=user_name)
    elif(predicted_class):
        print("predicted_class search")
        data=Data.objects.filter(predicted_class__exact=predicted_class)     
    elif(crop_type):
        print("crop_type search")
        data=Data.objects.filter(crop__exact=crop_type)
    else:
        print("location search")
        data=Data.objects.filter(latitude__lte=latitude+offset, latitude__gte=latitude-offset, longitude__lte=longitude+offset, longitude__gte=longitude-offset)
    
    response_data=[]
    for i in range(len(data)):
            data_dict={}
            data_dict["s_no"]=i+1
            data_dict["time_stamp"]=data[i].time_stamp
            data_dict["latitude"]=float(data[i].latitude)
            data_dict["longitude"]=float(data[i].longitude)
            data_dict["image_path"]=data[i].image_path
            data_dict["predicted_class"]=data[i].predicted_class
            data_dict["crop_type"]=data[i].crop_type.crop_name
            data_dict["user_name"]=data[i].user_name.user_name
            response_data.append(data_dict)


    context={"response_data":response_data}
    print(context)
    return render(request, 'developer/home.html', context)