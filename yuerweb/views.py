from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required


<<<<<<< HEAD
@login_required
def index(request):
    print("aaaaa")
=======

def index(request):
>>>>>>> 241a417dc80cfbc0dc622952f3889e40212160f3
    return render(request,'index.html')

def login(request):
    if list(request.session.values()) == []:
        return render(request,'login.html')
    else:
        return redirect('/')


def register(request):
    return render(request,'register.html')

def changepwd(request):
    return render(request,'changepwd.html')
