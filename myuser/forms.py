from django import forms
from captcha.fields import CaptchaField
from myuser.models import *

# Create your models here.
# 参考：https://cloud.tencent.com/developer/article/1091547
# 安装图片验证码：pip install django-simple-captcha


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128,
                               widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '输入验证码错误'})

    # def clean(self):
    #     # 验证码
    #     try:
    #         captcha_x = self.cleaned_data['captcha']
    #     except Exception as e:
    #         print('except: ' + str(e))
    #         raise forms.ValidationError(u"验证码有误，请重新输入")
    #
    #     # 用户名
    #     try:
    #         username = self.cleaned_data['username']
    #     except Exception as e:
    #         print('except: '+ str(e))
    #         raise forms.ValidationError(u"注册账号需为邮箱格式")
    #
    #     # 登录验证
    #     is_email_exist = User.objects.filter(email=username).exists()
    #     is_username_exist = User.objects.filter(username=username).exists()
    #     if is_username_exist or is_email_exist:
    #         raise forms.ValidationError(u"该账号已被注册")
    #
    #     # 密码
    #     try:
    #         password = self.cleaned_data['password']
    #     except Exception as e:
    #         print('except: ' + str(e))
    #         raise forms.ValidationError(u"请输入至少8位密码")
    #
    #     return self.cleaned_data

class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码', error_messages={'invalid': '输入验证码错误'})
