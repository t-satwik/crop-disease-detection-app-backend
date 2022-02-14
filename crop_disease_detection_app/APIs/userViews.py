
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import sys
import base64
import hashlib
import os
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponse

@api_view(['POST'])
def checkLogin(request):
    #send token when a new user is logged in
    try:
        data=request.data
        req_user_name=data['user_name']
        user = User.objects.filter(user_name=req_user_name)
        # print(req_user_name, req_password, user.password)
        if len(user) > 0:
            if 'password' in data:
                req_password=data['password']
                if(req_password == user[0].password):
                    return Response({'message':"User Verified"}, status=status.HTTP_200_OK)
                else:
                    return Response({'message':"Wrong Password"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message':"Enter pasword"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message':"User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def newSignup(request):
    #send token when a new user is created
    try:
        data = request.data
        user_obj = User()
        user_obj.user_name = data['user_name']
        user_obj.password=data['password']
        user_obj.email=data['email']
        user_obj.save()
        return Response({"message":"User Created"}, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST )

def clean_str(var):
    var.replace('/', '-')
    var.replace(' ', '_')
    var.replace(':', '-')
    return var

def get_image_path(self, folder_path):
    ts=clean_str(self.time_stamp)
    un=clean_str(self.user.user_name)
    ct=clean_str(self.crop_type.crop_name)
    file_name=un+'_'+ct+"_"+ts+'.png'
    return folder_path+file_name

@api_view(['POST'])
def setData(request):
    try:
        #replace conencting the user with user_name part with token
        data = request.data
        data_obj = Data()
        data_obj.time_stamp = data['time_stamp']
        data_obj.latitude = data['latitude']
        data_obj.longitude = data['longitude']
        data_obj.probability = data['probability']

        if( (data['predicted_class'], data['predicted_class']) in ALLOWED_PREDICTED_CLASSES):
            pc_obj=PredictedClass.objects.filter(predicted_class=data['predicted_class'])
            data_obj.predicted_class = pc_obj[0]
        else:
            return Response({"message":"predicted class not found"}, status=status.HTTP_404_NOT_FOUND)
        if( (data['crop_name'], data['crop_name']) in ALLOWED_CROP_TYPES):
            crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
            data_obj.crop_type = crop_obj[0]
        else:
            return Response({"message":"crop not found"}, status=status.HTTP_404_NOT_FOUND)
        user_obj=User.objects.filter(user_name=data['user_name'])
        if(len(user_obj)==0):
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            data_obj.user = user_obj[0]
        data_obj.image = data['image']
        data_obj.save()
        return Response({"message":"Data Object Created"}, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def setVideoFrame(request):
    try:
        data = request.data
        frame_obj = VideoFrame()
        frame_obj.time_stamp = data['time_stamp']
        frame_obj.start_latitude = data['start_latitude']
        frame_obj.end_latitude = data['end_latitude']
        frame_obj.start_longitude = data['start_longitude']
        frame_obj.end_longitude = data['end_longitude']
        
        frame_obj.probability = data['probability']

        if( (data['predicted_class'], data['predicted_class']) in ALLOWED_PREDICTED_CLASSES):
            pc_obj=PredictedClass.objects.filter(predicted_class=data['predicted_class'])
            frame_obj.predicted_class = pc_obj[0]
        else:
            return Response({"message":"predicted class not found"}, status=status.HTTP_404_NOT_FOUND)
        if( (data['crop_name'], data['crop_name']) in ALLOWED_CROP_TYPES):
            crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
            frame_obj.crop_type = crop_obj[0]
        else:
            return Response({"message":"crop not found"}, status=status.HTTP_404_NOT_FOUND)
        user_obj=User.objects.filter(user_name=data['user_name'])
        if(len(user_obj)==0):
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            frame_obj.user = user_obj[0]

        frame_obj.frame = data['image']
        frame_obj.save()
        frame_obj.save()
        return Response({"message":"Video Frame Saved"}, status=status.HTTP_200_OK )

    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def setSensorData(request):
    try:
        data = request.data
        sensor_data_obj = SensorValue()
        sensor_obj=Sensor()
        if( (data['sensor_type'], data['sensor_type']) in ALLOWED_SENSOR_TYPES):
            if(len(user_obj)==0):
                return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                sensor_data_obj.value = data['time_stamp']
                sensor_data_obj.latitude = data['latitude']
                sensor_data_obj.longitude = data['longitude']
                sensor_data_obj.time_stamp = data['time_stamp']
                latitude=data['latitude']
                longitude=data['longitude']
                offset=0.5
                sensors_in_offset=Sensor.objects.filter(latitude__lte=latitude+offset, latitude__gte=latitude-offset, longitude__lte=longitude+offset, longitude__gte=longitude-offset)
                sensors_type=Sensor.objects.filter(sensor_type=data['sensor_type'])
                flag=0
                for sensor in sensors_in_offset:
                    if sensor in sensors_type:
                        #existing sesnor found
                        flag=1
                        sensor_obj=sensor
                        sensor_data_obj.sensor = sensor_obj
                        sensor_data_obj.save()  #
                        return Response({"message":"Value Added to the sensor"}, status=status.HTTP_200_OK)
                if flag==0:
                        #new_sensor should be added
                        sensor_obj.sensor_type = data['sensor_type']
                        sensor_obj.longitude=data['longitude']
                        sensor_obj.latitude=data['latitude']
                        user_obj=User.objects.filter(user_name=data['user_name'])
                        sensor_obj.user = user_obj[0] 
                        sensor_data_obj.sensor = sensor_obj 
                        sensor_obj.save()  #save the sensor
                        sensor_data_obj.save() #save the sensor data
                        return Response({"message":"New sensor added and appended value"}, status=status.HTTP_200_OK)            
        else:
            return Response({"message":"sensor type not found"}, status=status.HTTP_404_NOT_FOUND)
            
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST )




@api_view(['POST'])
def getPastData(request):
    #update it to manage tokens, and also send only few frames per request, send multiple requests later
    try:
        data = request.data
        user_name = data['user_name']
        user_data=Data.objects.filter(user_name__exact=user_name)
        print(user_data)
        Response_dict={"message":"Data Fetch Successful", "data_count":str(len(user_data))}
        for i in range(len(user_data)):
            Response_dict["data"+str(i)]={}
            Response_dict["data"+str(i)]["time_stamp"]=user_data[i].time_stamp
            Response_dict["data"+str(i)]["latitude"]=user_data[i].latitude
            Response_dict["data"+str(i)]["longitude"]=user_data[i].longitude
            Response_dict["data"+str(i)]["encoded_image"]=user_data[i].encoded_image
            Response_dict["data"+str(i)]["predicted_class"]=user_data[i].predicted_class
            Response_dict["data"+str(i)]["crop_type"]=user_data[i].crop_type
            # return HttpResponse(user_data[i], content_type="image/png") Use this to send images maybe seperately
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )
