from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from users.models import Userinfo
from django.contrib.auth.decorators import login_required
import json
from baike.views import error

# Create your views here.

# 用户注册
def register(request):
    if request.method == 'POST':
        # TODO 查询用户信息并返回到登录界面
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        # 查询数据库中是否存在该数据
        user_pd = User.objects.filter(username=username).exists()
        if user_pd == True:
            data = {
                'code':400,
                'msg':'用户名已存在'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            # 创建用户
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user_save = Userinfo(
                user=user,
                phone=phone,
            )
            user_save.save()

            data = {
                'code': 200,
                'msg': '注册成功'
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

    return render(request, "register.html")


# 用户登录
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # 查询密码是否正确
            login(request,user)
            # print(request.session_id)
            # print(request.session['user_id'])
            # # request.session['is_login'] = True
            # # request.session['user_id'] =
            # # request.session['user_name'] = db_user.name

            data = {
                'code': 200,
                'msg': '登录成功'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {
                'code': 400,
                'msg': '登录失败'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, "login.html")


# 退出登录
def outlogin(request):
    request.session.flush()
    return redirect("/login")


@error
@login_required
def changepwd(request):
    print("aaaa")
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        data = {
            'code':200,
            'msg':'修改成功'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")



# 测试上传
def upload(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        avatar = request.FILES.get('avatar')
        print(avatar)
        with open(avatar.name, 'wb') as f:
            for line in avatar:
                f.write(line)
        return HttpResponse('ok')
    return render(request, 'picture_upload.html')


















