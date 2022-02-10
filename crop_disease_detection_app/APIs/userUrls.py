from django.urls import path, include
from .userViews import *

urlpatterns = [
   path('SetData/', setData),
   path('UserLogin/', checkLogin), 
   path('UserSignUp/', newSignup),
   path('GetPastData/', getPastData),
   path('SetVideoFrame/', setVideoFrame),
]