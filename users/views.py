from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from users.models import Userinfo,Follow
from django.contrib.auth.decorators import login_required
import json
from baike.views import error
from django.views.generic import View
from django.utils.decorators import method_decorator

# Create your views here.
from django.conf import settings
from sms import tengxun
import random


# 发送短信
def smsvif(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        yzmlist = list()
        for i in range(4):
            yzmlist.append(str(random.randint(0,9)))
        yzm = ''.join(yzmlist)

        request.session['smscode'] = yzm
        sms = tengxun.MySmsSender()
        sms.send(phone, settings.SMS_TEMPLATE_ID['register'], [yzm, '3'])
        data = {
            'code':200,
            'msg':'发送成功'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def center(request):
    return render(request,'center.html')

# 用户中心
@login_required
def centerMessage(request):
    return render(request,'centerMessage.html')

# 别人的个人中心
def centerhim(request):
    return render(request,'centerhim.html')


# 用户注册
def register(request):
    if request.method == 'POST':
        # TODO 查询用户信息并返回到登录界面
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        verification_Code = request.POST.get('verification_Code')
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

            # 获取验证码是否正确
            yzm = request.session['smscode']
            if verification_Code == yzm:
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
            else:
                data = {
                    'code': 400,
                    'msg': '验证码错误'
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
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


# 修改密码
@error
@login_required
def changepwd(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        data = {
            'code':200,
            'msg':'修改成功'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


# 修改头像
@login_required
def changetx(request):
    # avatar = request.POST.get('avatar')
    file_obj = request.FILES.get('avatar')
    Userinfo.user_avatar = file_obj
    Userinfo.save()
    print("ok")





#TODO 去TM的面向对象编程

# @method_decorator(error, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Followapi(View):
    def __init__(self,**kwargs):
        super(Followapi, self).__init__(**kwargs)

    def post(self,request):
        self.user = request.user
        print(self.user)
        self.request = request
        Quser_id = request.POST.get("Quser_id",None)
        if Quser_id == None:
            pass
        else:
            self.Quser = User.objects.get(id=int(Quser_id))
        type = int(request.POST.get('type'))
        if type == 0:
            return self.follow()
        elif type == 1:
            return self.unfollowapi()
        elif type == 2:
            return self.getfollowapi()
        elif type == 3:
            return self.getfollowedapi()
        else:
            return HttpResponse(json.dumps({'code':406,'msg':'参数错误'}))

    # 关注0
    def follow(self):
        f = Follow.objects.filter(follower=self.user, followed=self.Quser)
        if f:
            pass
        else:
            Follow.objects.create(
                follower=self.user,
                followed=self.Quser
            )
        data = {
            'code': 200,
            'msg': '已关注'
        }
        return HttpResponse(json.dumps(data))

    # 取消关注1
    def unfollowapi(self):
        Follow.unfollow(self.user, self.Quser)  # 取消关注
        data = {
            'code': 200,
            'msg': '已取消'
        }
        return HttpResponse(json.dumps(data))

    # 获得关所有已关注对象2
    def getfollowapi(self):
        follow_list = Follow.user_followed(self.user)
        print(follow_list)
        data = {
            'code': 200,
            'msg': '成功',
            'data_list': follow_list
        }
        return HttpResponse(json.dumps(data))

    # 获得粉丝3
    def getfollowedapi(self):
        follow_list = Follow.user_follower(self.user)
        data = {
            'code': 200,
            'msg': '成功',
            'data_list': follow_list
        }
        return HttpResponse(json.dumps(data))






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





