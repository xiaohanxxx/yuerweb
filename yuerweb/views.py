from django.shortcuts import render, HttpResponse, redirect



def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')


def register(request):
    return render(request,'register.html')

def changepwd(request):
    return render(request,'changepwd.html')
