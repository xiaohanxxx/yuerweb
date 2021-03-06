from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from users.models import Userinfo, Follow
from django.contrib.auth.decorators import login_required
from notifications.signals import notify
import json, random
from baike.views import error
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.conf import settings
from sms import tengxun
from luntan import models
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


# 发送短信
def smsvif(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        yzmlist = list()
        for i in range(4):
            yzmlist.append(str(random.randint(0, 9)))
        yzm = ''.join(yzmlist)

        request.session['smscode'] = yzm
        sms = tengxun.MySmsSender()
        a = sms.send(phone, settings.SMS_TEMPLATE_ID['register'], [yzm])
        print(a)
        data = {
            'code': 200,
            'msg': '发送成功'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def center(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo,user_id=user.id)
    level = userinfo.get_level_display()
    integral = userinfo.integral
    data = {
        'user': user,
        'level': level,
        'integral': integral,
        'userinfo': userinfo
    }
    return render(request, 'center.html', {'data': data})


# 用户中心
@login_required
def centerMessage(request):
    user = request.user
    userinfo = get_object_or_404(Userinfo,user_id=user.id)
    level = userinfo.get_level_display()
    integral = userinfo.integral
    data = {
        'user': user,
        'level': level,
        'integral': integral,
        'userinfo': userinfo
    }
    return render(request, 'centerMessage.html', {'data': data})


# 别人的个人中心
def centerhim(request, Quser_id):
    userinfo = get_object_or_404(Userinfo,user_id=Quser_id)
    level = userinfo.get_level_display()
    integral = userinfo.integral
    data = {
        'user': userinfo.user,
        'level': level,
        'integral': integral
    }
    return render(request, 'centerhim.html', {'data': data})


# 用户注册
@error
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
                'code': 400,
                'msg': '用户名已存在'
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            # 创建用户
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
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = {
                    'code': 400,
                    'msg': '验证码错误'
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, "register.html")


# 用户登录
@csrf_exempt
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证密码
        user = authenticate(username=username, password=password)
        if user:
            # 查询密码是否正确
            login(request, user)
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
        print('aaaaa')
        new_password = request.POST.get('new_password', None)
        if new_password == None:
            data = {
                'code': 400,
                'msg': '修改失败'
            }
        else:
            request.user.set_password(new_password)
            request.user.save()
            data = {
                'code': 200,
                'msg': '修改成功'
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



# TODO 去TM的面向对象编程
@method_decorator(error, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class Followapi(View):
    def __init__(self, **kwargs):
        super(Followapi, self).__init__(**kwargs)

    def post(self, request):
        self.user = request.user
        self.request = request
        Quser_id = request.POST.get("Quser_id", None)
        type = int(request.POST.get('type'))
        print(Quser_id, type)
        if Quser_id == None:
            pass
        else:
            self.Quser = User.objects.get(id=int(Quser_id))

        if type == 0:
            return self.follow()
        elif type == 1:
            return self.unfollowapi()
        elif type == 2:
            return self.getfollowapi()
        elif type == 3:
            return self.getfollowedapi()
        else:
            return HttpResponse(json.dumps({'code': 406, 'msg': '参数错误'}), content_type="application/json")

    # 关注0
    def follow(self):
        f = Follow.objects.filter(follower=self.user, followed=self.Quser)
        if f:
            data = {
                'code': 400,
                'msg': '你已经关注过该用户'
            }
        else:
            Follow.objects.create(
                follower=self.user,
                followed=self.Quser
            )
            data = {
                'code': 200,
                'msg': '已关注'
            }
        return HttpResponse(json.dumps(data), content_type="application/json")

    # 取消关注1
    def unfollowapi(self):
        Follow.unfollow(self.user, self.Quser)  # 取消关注
        data = {
            'code': 200,
            'msg': '已取消'
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    # 获得关所有已关注对象2
    def getfollowapi(self):
        follow_list = Follow.user_followed(self.user)
        for i in follow_list:
            article_list = models.Articles.objects.filter(user_id=i['userid'])
            print(article_list)

        data = {
            'code': 200,
            'msg': '成功',
            'data_list': list({
                                  'user': i['username'],
                                  'userid': i['userid'],
                                  'user_avatar':i['user_avatar'],
                                  'user_article': list(
                                      models.Articles.objects.filter(user_id=i['userid']).values('id', 'title'))
                              }
                              for i in follow_list
                              )
        }


        return HttpResponse(json.dumps(data), content_type="application/json")

    # 获得粉丝3
    def getfollowedapi(self):
        follow_list = Follow.user_follower(self.user)

        data = {
            'code': 200,
            'msg': '成功',
            'data_list': follow_list
        }
        return HttpResponse(json.dumps(data), content_type="application/json")


# 等级变更公用方法
def public_level(request):
    user = request.user
    userinfo = Userinfo.objects.get(user_id=user.id)
    integral = userinfo.integral
    if integral < 500:
        userinfo.level = 0
    elif integral > 500 and integral < 2000:  # 大于500且小于2000积分,白银
        userinfo.level = 1
    else:
        userinfo.level = 2
    userinfo.save()


# 公用通知方法
def noticate(user, recipient, target, message):
    # target 主题
    # message 评论消息
    notify.send(
        user,  # 消息发送者
        recipient=recipient,  # 消息接收者
        target=target,
        verb=message,  # 分情况；评论或回复
    )



# 获取通知信息
def getnoticate(request):
    return HttpResponse('ok')

# 忘记密码
@csrf_exempt
def forget(request):
    if request.method == "POST":
        #1、验证手机号码是否正确
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        verification_Code = request.POST.get('verification_Code')
        password = request.POST.get('newpassword')
        user = User.objects.filter(username=username)
        if user:
            obj = User.objects.get(username=username)
            userobj = Userinfo.objects.get(user_id=obj.id)
            if userobj.phone != phone:
                return HttpResponse(json.dumps({'code':400,'msg':'手机号与用户名不匹配'}), content_type="application/json")
            else:
                yzm = request.session['smscode']
                if verification_Code == yzm:
                    # 密码重置
                    obj.set_password(password)
                    obj.save()
                    return HttpResponse(json.dumps({'code':200,'msg':'密码已修改'}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'code':400,'msg':'没有此用户'}), content_type="application/json")
    return render(request,'forget.html')



# 测试上传
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        avatar = request.FILES.get('file')
        user = Userinfo.objects.get(user=request.user)
        user.user_avatar = avatar
        user.save()
    return HttpResponse(json.dumps({'code': 200}), content_type="application/json")


# 修改用户名
@error
@login_required
def set_username(request):
    user = request.user
    username = request.POST.get('username')
    user.username = username
    user.save()
    data = {
        'code':200,
        'msg':'修改成功'
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
