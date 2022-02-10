
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import sys
import base64
import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.http import HttpResponse

@api_view(['POST'])
def checkLogin(request):
    #send token when a new user is logged in
    try:
        data=request.data
        req_user_name=data['user_name']
        req_password=data['password']
        user = get_object_or_404(User, user_name=req_user_name)
        # print(req_user_name, req_password, user.password)
        if user is not None:
            if 'password' in data:
                if(req_password == user.password):
                    return Response({'message':"User Verified"}, status=status.HTTP_200_OK)
                else:
                    return Response({'message':"Wrong Password"}, status=status.HTTP_401_UNAUTHORIZED)
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

@api_view(['POST'])
def setData(request):
    try:
        #replace conencting the user with user_name part with token
        data = request.data
        data_obj = Data()
        data_obj.time_stamp = data['time_stamp']
        data_obj.latitude = data['latitude']
        data_obj.longitude = data['longitude']
        data_obj.predicted_class = data['predicted_class']
        data_obj.probability = data['probability']
        # data_obj.image = data['image']
        # user_obj=User.objects.filter(user_name=data['user_name'])
        # data_obj.user = user_obj[0]
        # crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
        # data_obj.crop_type = crop_obj[0]
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
        frame_obj.startLatitude = data['startLatitude']
        frame_obj.endLatitude = data['endLatitude']
        frame_obj.startLongitude = data['startLongitude']
        frame_obj.endLongitude = data['endLongitude']
        frame_obj.predicted_class = data['predicted_class']
        frame_obj.probability = data['probability']
        frame_obj.image = data['image']     
        user_obj=User.objects.filter(user_name=data['user_name'])
        frame_obj.user = user_obj[0]
        crop_obj=Crop.objects.filter(crop_name=data['crop_name'])
        frame_obj.crop_name = crop_obj[0]
        frame_obj.save()
        return Response({"message":"Video Frame Saved"}, status=status.HTTP_200_OK )

    except Exception:
        print(sys.exc_info())
        return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST )


# @api_view(['POST'])
# def userImgUpload(request):
#     try:
#         data = request.data
#         data_obj = DATA_wImg()
#         data_obj.image = data['image']
#         print(data['image'])
#         data_obj.save()
#         return Response({"message":"Image uploaded"}, status=status.HTTP_200_OK )
#     except:
#         return Response({"message":"Bad Request - python Exception"}, status=status.HTTP_400_BAD_REQUEST )

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
