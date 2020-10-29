from django.shortcuts import render,HttpResponse,redirect
from users import models as usermodels
import json
from datetime import datetime
# Create your views here.



# 注册
def register(request):
    if request.method == 'POST':
        # TODO 查询用户信息并返回到登录界面
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # 查询数据库中是否存在该数据
        user = usermodels.User.objects.filter(user_name=username).exists()
        if user == True:
            return HttpResponse(json.dumps({'validation':'repeat'}), content_type="application/json")
        else:
            # 创建用户
            try:
                usermodels.User.objects.create(
                    user_name=username,
                    user_pwd=password,
                    user_email=email,
                    user_phone=phone,
                    user_grade=0,
                    user_yuliang=5,
                    user_state=True,
                    add_time=datetime.now
                )
                data = {
                'validation':True, # 返回验证
                }
                return HttpResponse(json.dumps(data),content_type="application/json")
            except:
                return HttpResponse(json.dumps({'validation':False}), content_type="application/json")

    return render(request, "register.html")




# 登录
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # TODO 查询用户信息并返回重定向页面
        user = usermodels.User.objects.filter(user_name=username).exists()
        if user == True:
            # 查询密码是否正确
            userobj = usermodels.User.objects.get(user_name=username)
            if userobj.user_pwd == password:
                request.session['is_login'] = True
                request.session['user_name'] = username
                print(request.session['user_name'])
                print("返回主界面")
                return HttpResponse(json.dumps({'validation':True}), content_type="application/json")
            else:
                print("密码错误")
                return HttpResponse(json.dumps({'validation':False}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'validation':False}), content_type="application/json")

    else:
        return render(request, "login.html")


# 退出登录
def logout(request):
    request.session.flush()
    return redirect("/login")