from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    print("aaaaa")
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


def register(request):
    return render(request,'register.html')

def changepwd(request):
    return render(request,'changepwd.html')

