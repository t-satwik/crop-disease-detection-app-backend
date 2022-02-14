from django.urls import path, include
from .userViews import *

urlpatterns = [
   path('SetData/', setData),
   path('Login/', checkLogin), 
   path('SignUp/', newSignup),
   path('GetPastData/', getPastData),
   path('SetVideoFrame/', setVideoFrame),
   path('SetSensorData/', setSensorData),
]