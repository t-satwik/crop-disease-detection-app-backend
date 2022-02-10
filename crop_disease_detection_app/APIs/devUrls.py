from django.urls import path, include
from .devViews import *

urlpatterns = [
   path('login/', devLogin),
   path('home/', devHome)
]