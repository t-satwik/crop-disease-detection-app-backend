from django.urls import path, include
from .pageViews import *

urlpatterns = [
   path('', homePageView),
]