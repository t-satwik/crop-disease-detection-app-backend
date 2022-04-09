from .models import *
from django.shortcuts import get_object_or_404
import sys
import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages


def homePageView(request):
    return render(request, 'index.html')