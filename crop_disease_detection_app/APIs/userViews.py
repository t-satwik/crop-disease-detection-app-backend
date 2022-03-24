
from django.http import FileResponse
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

def get_image_path(obj):
    ts=clean_str(obj.time_stamp)
    un=clean_str(obj.user.user_name)
    ct=clean_str(obj.crop_type.crop_name)
    file_name=un+'_'+ct+"_"+ts+'.png'
    return file_name

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
        data_obj.file_name=get_image_path(data_obj)
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
        print("1")
        if( (data['sensor_type'], data['sensor_type']) in ALLOWED_SENSOR_TYPES):
            print("2")
            user_obj=User.objects.filter(user_name=data['user_name'])
            if(len(user_obj)==0):
                print("3")
                print("user 404")
                return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                sensor_data_obj.value = data['value']
                sensor_data_obj.latitude = data['latitude']
                sensor_data_obj.longitude = data['longitude']
                sensor_data_obj.time_stamp = data['time_stamp']
                latitude=float(data['latitude'])
                longitude=float(data['longitude'])
                sensor_data_obj.sensor_type=data['sensor_type']
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
                        sensor_obj.user = user_obj[0]
                        sensor_data_obj.sensor = sensor_obj 
                        sensor_obj.save()  #save the sensor
                        sensor_data_obj.save() #save the sensor data
                        return Response({"message":"New sensor added and appended value"}, status=status.HTTP_200_OK)            
        else:
            print("sensor 404")
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
        user_data=Data.objects.filter(user__exact=user_name)
        # print(user_name)
        num=1
        Response_dict={"message":"Data Fetch Successful", "data_count":str(num)}
        # print("0")
        for i in range(int(data['starting_index']), int(data['starting_index'])+num):
            # print("1")
            if(i>=len(user_data)):
                break
            Response_dict["data"+str(i)]={}
            Response_dict["data"+str(i)]["time_stamp"]=user_data[i].time_stamp
            Response_dict["data"+str(i)]["latitude"]=user_data[i].latitude
            Response_dict["data"+str(i)]["longitude"]=user_data[i].longitude
            Response_dict["data"+str(i)]["predicted_class"]=user_data[i].predicted_class.predicted_class
            Response_dict["data"+str(i)]["probability"]=user_data[i].probability
            Response_dict["data"+str(i)]["user"]=user_data[i].user.user_name
            Response_dict["data"+str(i)]["crop_type"]=user_data[i].crop_type.crop_name
            # f = open(user_data[i].image, "rb")
            Response_dict["data"+str(i)]["encoded_image"]=base64.b64encode(user_data[i].image.read())
            Response_dict["data"+str(i)]["file_name"]=user_data[i].file_name
            # filename=user_data[i].image.name
            # img = open(filename, 'rb')
            # print(user_data[i].image)
            # Response_dict["data"+str(i)]["image"]=user_data[i].image
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def getSensorsData(request):
    #update it to manage tokens, and also send only few frames per request, send multiple requests later
    try:
        data = request.data
        user_name = data['user_name']
        user_data=SensorValue.objects.filter(user__exact=user_name)
        # print(user_name)
        num=2
        Response_dict={"message":"Sensors Data Fetch Successful index:", "total_count":str(len(user_data))}
        # print("0")
        for i in range(len(user_data)):
            # print("1")
            Response_dict["sensor"+str(i)]={}
            Response_dict["sensor"+str(i)]["sensor_type"]=user_data[i].sensor_type
            Response_dict["sensor"+str(i)]["latitude"]=user_data[i].latitude
            Response_dict["sensor"+str(i)]["longitude"]=user_data[i].longitude
            Response_dict["sensor"+str(i)]["user"]=user_data[i].user.user_name
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def getSensorValuesData(request):
    #update it to manage tokens, and also send only few frames per request, send multiple requests later
    try:
        data = request.data
        user_name = data['user_name']
        user_sensors=Sensor.objects.filter(user__exact=user_name)
        user_data=[]
        for sensor in user_sensors:
            user_data.extend(SensorValue.objects.filter(sensor__exact=sensor))
        # print(user_name)
        Response_dict={"message":"Data Values Fetch Successful", "total_count":str(len(user_data))}
        # print("0")
        for i in range(len(user_data)):
            # print("1")
            Response_dict["value"+str(i)]={}
            Response_dict["value"+str(i)]["value"]=user_data[i].value
            Response_dict["value"+str(i)]["latitude"]=user_data[i].latitude
            Response_dict["value"+str(i)]["longitude"]=user_data[i].longitude
            Response_dict["value"+str(i)]["time_stamp"]=user_data[i].time_stamp
            Response_dict["value"+str(i)]["sensor_type"]=user_data[i].sensor_type            
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

@api_view(['POST'])
def getClimateData(request):
    try:
        data = request.data
        latitude = data['latitude']
        longitude = data['longitude']
        user_name = data['user_name']
        data_present=False
        print(len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="phosphorus")))
        if(len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="nitrogen"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="phosphorus"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="potassium"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="pH"))>0):
            data_present=True
        if(data_present):
            Response_dict={"message":"Climate Values Fetch Successful", "full_data":1}
            for value_type in ['nitrogen', 'phosphorus', 'potassium', 'pH']: #Computing the average for each
                sensors=Sensor.objects.filter(user__exact=user_name, sensor_type__exact=value_type)
                value_sum=0
                count=0
                for sensor in sensors:
                    SensorValue_data=SensorValue.objects.filter(sensor__exact=sensor)
                    for v in range(len(SensorValue_data)):
                        value_sum+=SensorValue_data[v].value
                        count+=1
                if(count==0):
                    Response_dict["message"]="Bad Request - No Data Present"
                    count=1
                value_avg=value_sum/count
                Response_dict[value_type]=value_avg                       
        else:
            Response_dict={"message":"Climate Values Fetch Successful", "full_data":0}
        #TODO: Fetch Climate data using APIS and assign them to avg_temp, avg_humidity, avg_rainfall
        avg_temp=0
        avg_humidity=0
        avg_rainfall=0
        Response_dict["temperature"]=avg_temp
        Response_dict["humidity"]=avg_humidity
        Response_dict["rainfall"]=avg_rainfall      
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )
