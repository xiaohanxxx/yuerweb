from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from users.models import Userinfo
from django.contrib.auth.decorators import login_required
import json

# Create your views here.


    def clean_user_phone(self):
        val = self.cleaned_data.get("user_phone")
        if len(val) == 11:  # 判断长度
            return val
        else:
            raise ValidationError("手机号码必须11位")

    def clean(self):  # 全局钩子
        pwd = self.cleaned_data.get("user_pwd")
        r_pwd = self.cleaned_data.get("r_user_pwd")
        if pwd and r_pwd and pwd != r_pwd:
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


class LoginForm(forms.Form):
    user_name = forms.fields.CharField(
        max_length=24,
        min_length=6,
    )

    user_pwd = forms.fields.CharField(
        max_length=32,
        min_length=6,
        error_messages={
            'required': "密码不能为空",
            'min_length': "密码长度不能小于6",
            'max_length': "密码长度不能大于32"
        },
        widget=forms.widgets.PasswordInput()
    )

    def clean(self):  # 全局钩子
        name = self.cleaned_data.get('user_name')
        try:
            user_data = usermodels.User.objects.get(user_name=name)
        except:
            raise ValidationError("用户名不存在")

        pwd = self.cleaned_data.get("user_pwd")
        if pwd != user_data.user_pwd:
            raise ValidationError("两次密码不一致")
        else:
            # 创建用户
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user_save = Userinfo(
                phone=phone,
            )
            user_save.save()

            data = {
                'code': 200,
                'msg': '注册成功'
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

    return render(request, "register.html")

        data = form.cleaned_data
        request.session['is_login'] = True
        request.session['user_id'] = data['user_id']
        return render(request, 'index.html')


# 退出登录
def outlogin(request):
    request.session.flush()
    return redirect("/login")


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


















