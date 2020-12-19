from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from webmanage import models

def index(request):

    # 返回友情链接
    friend_link = [i for i in models.FriendLink.objects.all().order_by('idx').values('link_name','link','idx')]
    # print(friend_link)
    return render(request,'index.html',{"friendlink":friend_link})

def login(request):
    if list(request.session.values()) == []:
        return render(request,'login.html')
    else:
        return redirect('/')

def register(request):
    return render(request,'register.html')

def changepwd(request):
    return render(request,'changepwd.html')


# 移动端
def m_index(request):
    return render(request,'m_template/index.html')

def m_login(request):
    return render(request,'m_template/login.html')

def m_zhuce(request):
    return render(request,'m_template/zhuce.html')

def m_forget(request):
    return render(request,'m_template/forget.html')