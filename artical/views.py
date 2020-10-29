from django.shortcuts import render

# Create your views here.
import json
from django import views
from django.shortcuts import render, HttpResponse
from . import models



def index(request):
    print("aaaaaaaaaaaaaaaaaa")
    return render(request,'index.html')