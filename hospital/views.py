from django.shortcuts import render,HttpResponse

# Create your views here.

def hospital(request):
    # return render(request,'hospital.html')
    return HttpResponse("医院推荐")