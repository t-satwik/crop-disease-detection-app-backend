
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
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split
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
                return Response({'message':"Enter Pasword"}, status=status.HTTP_401_UNAUTHORIZED)
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
    var=var.replace('/', '-')
    var=var.replace(' ', '_')
    var=var.replace(':', '-')
    return var

def get_image_path(obj):
    ts=clean_str(obj.time_stamp)
    un=clean_str(obj.user.user_name)
    ct=clean_str(obj.crop_type.crop_name)
    file_name=un+"_"+ct+"_"+ts+".png"
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
            print(data['predicted_class'])
            return Response({"message":"predicted class not found"}, status=status.HTTP_404_NOT_FOUND)
        if( (data['crop_name'], data['crop_name']) in ALLOWED_CROP_TYPES):
            crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
            data_obj.crop_type = crop_obj[0]
        else:
            print(data['crop_name'])
            return Response({"message":"crop not found"}, status=status.HTTP_404_NOT_FOUND)
        user_obj=User.objects.filter(user_name=data['user_name'])
        if(len(user_obj)==0):
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            data_obj.user = user_obj[0]
        data_obj.image = data['image']
        file_name=get_image_path(data_obj)
        # print(file_name)
        data_obj.file_name=file_name
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
            # print(data['predicted_class'])
            return Response({"message":"predicted class not found"}, status=status.HTTP_404_NOT_FOUND)
        if( (data['crop_name'], data['crop_name']) in ALLOWED_CROP_TYPES):
            crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
            frame_obj.crop_type = crop_obj[0]
        else:
            print(data['crop_name'])
            return Response({"message":"crop not found"}, status=status.HTTP_404_NOT_FOUND)
        user_obj=User.objects.filter(user_name=data['user_name'])
        if(len(user_obj)==0):
            return Response({"message":"user not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            frame_obj.user = user_obj[0]
        frame_obj.image = data['image']
        file_name=get_image_path(frame_obj)
        # print(file_name)
        frame_obj.file_name=file_name
        frame_obj.save()
        return Response({"message":"Frame Object Created"}, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

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
                print("3")
                sensor_data_obj.value = data['value']
                sensor_data_obj.latitude = data['latitude']
                sensor_data_obj.longitude = data['longitude']
                sensor_data_obj.time_stamp = data['time_stamp']
                latitude=float(data['latitude'])
                longitude=float(data['longitude'])
                sensor_data_obj.sensor_type=data['sensor_type']
                offset=0.001
                sensors_in_offset=Sensor.objects.filter(latitude__lte=latitude+offset, latitude__gte=latitude-offset, longitude__lte=longitude+offset, longitude__gte=longitude-offset)
                sensors_type=Sensor.objects.filter(sensor_type=data['sensor_type'])
                sensors_type=Sensor.objects.filter(user=user_obj[0])
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
        print(len(user_data))
        num=3
        Response_dict={"message":"Data Fetch Successful"}
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
            # Response_dict["data"+str(i)]["encoded_image"]=base64.b64encode(user_data[i].image.read())
            Response_dict["data"+str(i)]["file_name"]=user_data[i].file_name
            print(user_data[i].file_name)
            # filename=user_data[i].image.name
            # img = open(filename, 'rb')
            # print(user_data[i].image)
            # Response_dict["data"+str(i)]["image"]=user_data[i].image
        Response_dict["max_index"]=i
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
        Response_dict={"message":"Sensors Data Fetch Successful", "total_count":str(len(user_data))}
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

def get_rainfall_val(latitude, longitude):
    data=[['Srikakulam', (18.6, 84.3), 1199.0142857142857], ['Visakhapatnam', (17.7, 83.3), 1176.2714285714285], ['East Godavari', (17.0, 82.2), 1197.542857142857], ['West Godavari', (16.8, 81.5), 1166.4571428571428], ['Krishna', (16.2, 81.1), 1162.6857142857145], ['Guntur', (16.6, 79.6), 952.3714285714286], ['Nellore', (14.5, 80.0), 1183.7857142857142], ['Kurnool', (15.8, 78.1), 780.6285714285715], ['Ananthapur', (14.6, 77.0), 696.4142857142858], ['Chittoor', (13.5, 78.5), 1011.157142857143], ['Muzaffarpur', (26.1, 85.4), 527.16], ['Ahmedabad', (23.1, 72.6), 836.2833333333334], ['Amreli', (21.5, 71.1), 824.9142857142858], ['Banaskantha', (24.3, 71.9), 759.9571428571428], ['Bhavnagar', (21.8, 72.2), 740.3000000000001], ['Valsad', (20.6, 73.2), 2272.657142857143], ['Dangs', (20.8, 73.6), 2404.5142857142855], ['Jamnagar', (22.5, 70.1), 873.2714285714286], ['Kheda', (22.3, 73.3), 940.2428571428572], ['Kutch', (23.3, 69.8), 501.64285714285717], ['Mehsana', (23.8, 71.6), 914.9571428571428], ['Panchmahal', (22.9, 73.8), 876.8999999999999], ['Rajkot', (22.3, 70.8), 847.5428571428572], ['Sabarkantha', (23.5, 73.2), 1003.2714285714286], ['Surat', (21.2, 72.1), 1808.857142857143], ['Surendranagar', (22.8, 71.6), 656.1999999999999], ['Hissar', (29.2, 75.7), 372.22857142857146], ['Gurgaon', (28.5, 76.8), 565.9200000000001], ['Jind', (29.5, 76.4), 556.3166666666667], ['Ambala', (30.4, 76.7), 970.2142857142859], ['Karnal', (29.7, 77.0), 605.7857142857143], ['Rohtak', (28.9, 76.6), 470.91428571428565], ['Kolar', (13.1, 78.1), 839.6714285714286], ['Tumkur', (13.4, 77.1), 845.2142857142857], ['Mysore', (12.1, 76.3), 831.8571428571429], ['Mandya', (12.8, 77.8), 792.4571428571428], ['Hassan', (13.0, 76.2), 1184.3714285714286], ['Chitradurga', (14.2, 76.4), 727.5], ['Bellary', (15.2, 76.9), 677.4428571428572], ['Dharwad', (15.5, 75.0), 817.6428571428571], ['Bidar', (17.9, 77.5), 885.8285714285713], ['Raichur', (16.2, 77.4), 708.7714285714286], ['Jabalpur', (23.0, 80.0), 1252.7], ['Balaghat', (22.1, 80.6), 1357.4142857142856], ['Narsinghpur', (22.8, 79.0), 1098.5714285714287], ['Mandla', (25.0, 88.1), 1272.642857142857], ['Sagar', (23.9, 78.8), 1061.0], ['Damoh', (24.1, 79.6), 1070.142857142857], ['Tikamgarh', (24.9, 78.9), 704.5], ['Chhatarpur', (25.1, 79.5), 833.6142857142859], ['Panna', (24.3, 80.0), 890.5500000000001], ['Rewa', (24.5, 81.3), 808.5799999999999], ['Sidhi', (24.3, 82.0), 771.0333333333333], ['Satna', (24.6, 80.1), 911.6285714285714], ['Shahdol', (23.5, 81.1), 1011.0], ['Gwalior', (26.2, 78.3), 678.0285714285714], ['Shivpuri', (24.6, 77.5), 704.6428571428571], ['Guna', (24.7, 77.3), 846.2285714285715], ['Datia', (25.7, 78.5), 683.8666666666668], ['Morena', (25.1, 76.7), 650.9666666666667], ['Bhind', (21.9, 77.7), 595.2571428571429], ['Indore', (22.7, 75.8), 896.9857142857144], ['Ratlam', (23.0, 75.0), 944.9714285714284], ['Ujjain', (23.3, 75.7), 947.5428571428572], ['Mandsaur', (24.3, 75.2), 886.6714285714286], ['Dewas', (22.6, 76.4), 768.46], ['Dhar', (22.5, 75.0), 824.0571428571428], ['Jhabua', (22.6, 74.4), 904.8571428571429], ['Sehore', (22.9, 77.1), 963.5400000000002], ['Raisen', (23.2, 78.2), 988.9142857142857], ['Vidisha', (23.9, 77.9), 996.3285714285714], ['Betul', (21.9, 77.9), 1058.6333333333334], ['Rajgarh', (23.9, 76.8), 803.9666666666667], ['Shajapur', (23.4, 76.4), 894.1142857142858], ['Hoshangabad', (22.8, 77.8), 1305.6142857142859], ['Bombay', (18.9, 72.8), 2625.7571428571428], ['Thane', (20.0, 72.7), 2843.1571428571433], ['Raigad', (18.4, 73.1), 3450.085714285714], ['Ratnagiri', (17.0, 73.0), 3525.9], ['Nasik', (20.6, 74.5), 1252.042857142857], ['Jalgaon', (21.1, 75.6), 733.7285714285715], ['Ahmednagar', (19.1, 74.9), 689.657142857143], ['Pune', (18.5, 73.9), 978.0285714285714], ['Satara', (17.4, 73.6), 1226.257142857143], ['Sangli', (16.9, 74.8), 811.5428571428571], ['Kolhapur', (16.7, 74.2), 2222.6428571428573], ['Aurangabad', (19.9, 75.3), 768.8285714285714], ['Parbhani', (19.1, 76.1), 887.3428571428574], ['Beed', (19.0, 75.8), 711.157142857143], ['Nanded', (19.1, 77.2), 736.2333333333335], ['Osmanabad', (18.0, 76.1), 771.5], ['Akola', (20.7, 77.0), 836.342857142857], ['Yeotmal', (20.4, 78.1), 949.7142857142857], ['Wardha', (20.9, 78.4), 1045.8285714285714], ['Nagpur', (21.2, 79.1), 1080.6857142857145], ['Bhandara', (20.0, 79.3), 1308.8333333333333], ['Chandrapur', (19.4, 80.0), 1236.5571428571432], ['Balasore', (21.1, 86.9), 1771.3], ['Bolangir', (20.3, 83.2), 1397.8428571428572], ['Cuttack', (20.8, 85.9), 1762.314285714286], ['Dhenkanal', (20.7, 85.6), 1398.1285714285714], ['Ganjam', (19.3, 84.9), 1300.642857142857], ['Kalahandi', (19.3, 83.1), 1616.9], ['Koraput', (18.8, 82.7), 1938.642857142857], ['Puri', (19.8, 85.8), 1515.0714285714282], ['Sambalpur', (21.5, 84.0), 1392.7857142857142], ['Sundargarh', (21.5, 84.9), 1332.0285714285715], ['Gurdaspur', (32.3, 75.7), 969.4142857142858], ['Amritsar', (31.6, 74.9), 604.5714285714286], ['Kapurthala', (31.1, 75.4), 540.4], ['Jalandhar', (31.5, 75.6), 626.1714285714286], ['Hoshiarpur', (31.6, 75.9), 644.0285714285714], ['Ludhiana', (30.9, 75.9), 561.0428571428571], ['Ferozpur', (30.9, 74.6), 250.09999999999997], ['Bhatinda', (31.6, 75.3), 370.65714285714284], ['Sangrur', (31.0, 75.9), 340.54285714285714], ['Patiala', (30.0, 76.5), 733.1], ['Ajmer', (26.5, 74.6), 456.1714285714285], ['Alwar', (26.4, 76.6), 616.5857142857143], ['Banswara', (23.6, 74.5), 957.3142857142858], ['Barmer', (25.8, 71.4), 325.3], ['Bharatpur', (26.7, 77.9), 583.1571428571428], ['Bhilwara', (25.6, 74.9), 615.0], ['Bikaner', (28.0, 73.3), 267.45714285714286], ['Bundi', (25.6, 75.7), 535.8142857142857], ['Chittorgarh', (24.8, 75.5), 795.5142857142856], ['Churu', (28.4, 74.4), 350.87142857142857], ['Dungarpur', (23.8, 73.9), 785.2714285714285], ['Jaipur', (26.9, 75.8), 501.0], ['Jaisalmer', (26.9, 70.9), 220.5285714285714], ['Jalore', (25.1, 72.2), 438.38571428571424], ['Jhalawar', (24.5, 76.2), 741.8571428571429], ['Jhunjhunu', (28.1, 75.5), 427.19999999999993], ['Jodhpur', (26.3, 73.1), 266.7285714285714], ['Kota', (25.2, 75.9), 723.342857142857], ['Nagaur', (27.0, 74.0), 320.5142857142858], ['Pali', (25.7, 73.6), 403.7857142857143], ['Sikar', (27.6, 75.1), 391.6], ['Sirohi', (1.1, 24.7), 861.6428571428571], ['Tonk', (26.1, 75.6), 453.42857142857144], ['Udaipur', (24.6, 73.7), 710.1], ['Salem', (11.7, 78.0), 1046.3999999999999], ['Coimbatore', (11.0, 77.0), 914.6285714285714], ['Thanjavur', (10.8, 79.9), 1243.0142857142857], ['Madurai', (9.9, 78.1), 968.5714285714286], ['Kanyakumari', (8.3, 77.3), 1328.7857142857142], ['Chennai', (13.1, 80.2), 1476.9], ['Saharanpur', (29.9, 77.9), 994.6], ['Meerut', (29.0, 77.7), 487.6], ['Aligarh', (27.9, 78.1), 511.58000000000004], ['Mathura', (27.6, 77.6), 498.3166666666668], ['Agra', (27.2, 78.0), 409.92857142857144], ['Mainpuri', (27.3, 79.1), 591.8333333333334], ['Etah', (27.6, 78.8), 473.66], ['Bareilly', (28.4, 79.4), 1011.342857142857], ['Moradabad', (28.7, 78.7), 960.5799999999999], ['Shahjahanpur', (28.0, 79.9), 771.98], ['Pilibhit', (28.5, 79.9), 1146.9], ['Rampur', (28.8, 79.1), 620.95], ['Bijnor', (28.7, 78.7), 1000.7666666666668], ['Farrukhabad', (27.2, 79.5), 767.3599999999999], ['Etawah', (27.1, 78.7), 517.74], ['Fatehpur', (25.9, 80.1), 570.25], ['Allahabad', (25.5, 81.7), 831.1999999999999], ['Jhansi', (25.5, 78.6), 637.5833333333334], ['Jalaun', (26.0, 79.5), 668.1999999999999], ['Hamirpur', (25.5, 79.9), 975.9461538461536], ['Banda', (25.5, 80.4), 786.68], ['Varanasi', (25.3, 83.0), 685.6833333333333], ['Jaunpur', (25.7, 82.6), 648.65], ['Ghazipur', (25.7, 83.6), 652.1400000000001], ['Ballia', (25.9, 84.0), 586.2], ['Gorakhpur', (26.8, 83.4), 1269.4571428571428], ['Deoria', (26.8, 83.9), 804.1666666666666], ['Basti', (26.8, 82.8), 824.4], ['Azamgarh', (26.0, 83.2), 963.075], ['Lucknow', (26.9, 80.9), 880.4714285714286], ['Unnao', (26.6, 80.5), 665.8000000000001], ['Sitapur', (27.6, 80.8), 947.36], ['Hardoi', (27.4, 80.1), 723.34], ['Kheri', (27.9, 80.8), 1026.1], ['Faizabad', (26.5, 82.4), 902.1], ['Gonda', (27.1, 82.0), 921.3000000000001], ['Bahraich', (27.6, 81.6), 1175.6833333333334], ['Sultanpur', (26.2, 82.0), 805.1142857142858], ['Pratapgarh', (25.8, 81.8), 616.76], ['Barabanki', (26.9, 81.3), 780.375], ['Nadia', (23.4, 88.5), 1171.35], ['Murshidabad', (24.1, 88.3), 1146.0], ['Burdwan', (23.2, 87.9), 1142.9], ['Birbhum', (23.7, 87.7), 1131.25], ['Bankura', (24.4, 87.2), 1170.35], ['Hooghly', (22.9, 88.3), 1094.75], ['Howrah', (22.6, 88.0), 1276.1], ['Jalpaiguri', (26.5, 88.7), 3642.0], ['Darjeeling', (27.1, 88.3), 3273.85], ['Malda', (25.0, 88.1), 1257.4], ['Purulia', (23.0, 86.4), 1033.55], ['Durg', (21.2, 81.3), 967.0333333333333], ['Bastar', (19.1, 82.0), 1441.7285714285715], ['Raipur', (21.2, 81.7), 1157.142857142857], ['Bilaspur', (22.1, 82.1), 1144.4928571428572], ['Raigarh', (21.9, 83.4), 1165.4142857142856], ['Surguja', (23.1, 83.2), 966.3571428571429], ['Hazaribagh', (24.0, 85.4), 1034.7], ['Dhanbad', (23.8, 86.4), 879.9], ['Palamau', (24.1, 84.1), 870.76], ['Ranchi', (23.4, 85.0), 1257.042857142857], ['Nainital', (29.5, 79.7), 1551.5666666666668], ['Chamoli', (30.5, 79.7), 1336.3], ['Dehradun', (30.3, 78.0), 2211.457142857143], ['Cachar', (3.2, 24.5), 2876.5571428571425], ['Darrang', (26.9, 92.2), 1938.1166666666668], ['Dibrugarh', (27.3, 94.5), 2372.514285714286], ['Goalpara', (26.1, 90.4), 2405.62], ['Kamrup', (26.1, 91.4), 1621.2333333333333], ['Karbi Anglong', (25.5, 93.3), 1161.6166666666668], ['Lakhimpur', (27.1, 94.1), 2862.433333333333], ['Sibsagar', (26.6, 94.4), 1751.9666666666665], ['Chamba', (32.6, 76.4), 860.9499999999999], ['Kangra', (31.9, 76.5), 1545.3857142857144], ['Kinnaur', (31.6, 78.2), 605.5285714285714], ['Solan', (30.6, 76.8), 1094.8142857142857], ['Mandi', (31.6, 76.8), 1274.4714285714285], ['Kottayam', (9.4, 76.3), 3166.171428571429], ['Kozhikode', (11.2, 75.5), 3612.128571428572], ['Kollam', (8.5, 76.4), 2515.5999999999995], ['Thrissur', (10.3, 76.2), 3118.642857142858], ['Thiruvananthapuram', (8.3, 76.6), 1995.8857142857144], ['Hyderabad', (17.5, 78.5), 931.0571428571428], ['Nizamabad', (18.1, 78.1), 965.2571428571429], ['Medak', (17.6, 78.0), 866.0428571428572], ['Warangal', (18.0, 79.6), 1083.0857142857144], ['Khammam', (17.7, 80.9), 1340.2571428571428], ['Karimnagar', (18.4, 79.0), 1138.2857142857142]]
    min_distance=10000000000
    for district in data:
        curr_distance=latitude-district[1][0]**2+(longitude-district[1][1])**2
        if(curr_distance<min_distance):
            min_distance=curr_distance
            min_district=district
    # print(min_district, min_distance)
    return min_district[-1]

def recommend_crop(feature_values:list):
    path="https://drive.google.com/uc?export=download&id=1e_J4ObhvpdBsTXaH3wdwFH5oj78GT1wB"
    data=pd.read_csv(path) 
    data.head()
    data.shape
    x=data[['N','P','K','temperature','humidity','ph','rainfall']]
    y=data['label']
    train_x,test_x,train_y,test_y=train_test_split(x,y, train_size=0.9)
    c=0.01
    ker="linear"
    current_svc=SVC(C=c,kernel=ker)
    current_svc.fit(train_x.values, train_y.values)
    predict_value=current_svc.predict([feature_values])
    return predict_value


@api_view(['POST'])
def getCropRecommendation(request):
    try:
        data = request.data
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        user_name = data['user_name']
        avg_values={}
        avg_rainfall=get_rainfall_val(latitude, longitude)
        data_present=False
        # print(len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="phosphorus")))
        if(len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="nitrogen"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="phosphorus"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="potassium"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="pH"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="temperature"))>0) and \
          (len(Sensor.objects.filter(user__exact=user_name, sensor_type__exact="humidity"))>0):
            data_present=True
        if(data_present):
            Response_dict={"message":"Data present", "full_data":1}
            for value_type in ['nitrogen', 'phosphorus', 'potassium', 'pH', 'temperature', 'humidity']: #Computing the average for each
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
                    return Response(Response_dict, status=status.HTTP_200_OK )
                    count=1
                value_avg=value_sum/count
                avg_values[value_type]=float(value_avg)
            # print([avg_values['nitrogen'], avg_values['phosphorus'], avg_values['potassium'], avg_values['temperature'],avg_values['humidity'], avg_values['pH'], avg_rainfall])
            predicted_crop=recommend_crop([avg_values['nitrogen'], avg_values['phosphorus'], avg_values['potassium'], avg_values['temperature'],avg_values['humidity'], avg_values['pH'], avg_rainfall])
            Response_dict["predicted_crop"]=predicted_crop[0]
        else:
            Response_dict={"message":"Data not present", "full_data":0}
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )


@api_view(['POST'])
def getCropRecommendationWithGivenData(request):
    try:
        data = request.data
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        user_name = data['user_name']
        avg_rainfall=get_rainfall_val(latitude, longitude)
        nitrogen = float(data['nitrogen'])
        phosphorus = float(data['phosphorus'])
        potassium = float(data['potassium'])
        pH = float(data['pH'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        predicted_crop=recommend_crop([nitrogen, phosphorus, potassium, temperature, humidity, pH, avg_rainfall])
        Response_dict={"message":"Crop recommended successfully", "full_data":1}
        print(predicted_crop, type(predicted_crop))
        Response_dict["predicted_crop"]=predicted_crop[0]
        return Response(Response_dict, status=status.HTTP_200_OK )
    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )
