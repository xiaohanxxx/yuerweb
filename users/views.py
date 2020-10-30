from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from users import models as usermodels
import json
from datetime import datetime
from django import views, forms


# Create your views here.
class RegisterForm(forms.Form):
    user_name = forms.fields.CharField(
        max_length=24,
        min_length=6,
        error_messages={
            "required": "用户名不能为空",
            'min_length': "长度小于6",
            'max_length': "长度大于32",
        })
    user_email = forms.fields.EmailField(
        error_messages={
            'required': "邮箱不能为空",
            "invalid": "邮箱格式错误",
        }
    )
    user_phone = forms.fields.CharField(
        max_length=11
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
    r_user_pwd = forms.CharField(
        max_length=32,
        min_length=6,
        error_messages={
            'required': "密码不能为空",
            'min_length': "密码长度不能小于6",
            'max_length': "密码长度不能大于32"
        },
        widget=forms.widgets.PasswordInput())

    def clean_user_name(self):
        name = self.cleaned_data.get('user_name')
        isHave = usermodels.User.objects.filter(user_name=name)
        if isHave:
            raise ValidationError("用户名已存在")
        else:
            return name

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
            self.cleaned_data['user_id'] = user_data.pk
            return self.cleaned_data


# 注册
class Register(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html")

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html", {"form_obj": form.errors})

        # 创建用户
        data = form.cleaned_data
        data.pop('r_user_pwd')
        usermodels.User.objects.create(**data)
        return HttpResponse("注册成功！！！！！")


# 登录
class Login(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "register.html")

        data = form.cleaned_data
        request.session['is_login'] = True
        request.session['user_id'] = data['user_id']
        return render(request, 'index.html')


# 退出登录
class LoginOut(views.View):
    def get(self, request, *args, **kwargs):
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


















