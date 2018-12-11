from django.shortcuts import render, redirect
from django.db import models
import hashlib
from myuser import models
from myuser import forms
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# Create your views here.

def hash_code(s, salt='myuser'):  # 加盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    pass
    return render(request, 'myuser/index.html')

def login(request):
    """
    使用session就用户登录状态
    :param request: 
    :return: 
    """
    # 使用session防止重复登录
    if request.session.get('is_login', None):
        return redirect('/myuser/index')

    # 验证码密钥和图片
    hashkey = CaptchaStore.generate_key()
    # image_url = captcha_image_url(hashkey)

    if request.method == 'POST':
        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 用户名字合法性验证
            # 密码长度验证
            try:
                user = models.User.objects.get(name=username)
                # if user.password == password:
                if user.password == hash_code(password):  # 使用哈希值与数据库的值进行比较
                    # 向session字典写入用户组状态和数据(可以写任何数据)
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/myuser/index')
                else:
                    message = '密码不正确'
            except:
                message = "用户不存在"

        # 增加了message变量，用于保存提示信息。当有错误信息的时候，将错误信息打包成一个字典，然后作为第三个参数提供给render()方法
        return render(request, 'myuser/login.html', locals())
    login_form = forms.UserForm()
    # locals()是python的内置函数，返回当前所有的本地变量字典
    # 此处：locals就等于：{'message':message, 'login_form':login_form}
    return render(request, 'myuser/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就没有登录，就没有登出一说
        return redirect('/myuser/index')
    request.session.flush()  # 一次性将session中的所有内容全部清空，不留后患
    # 或者使用一下方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return render(request, 'myuser/index.html')

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/myuser/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        print('request.method == ', "POST")
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            print('register email is:', email)
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'myuser/register.html', locals())
            else:
                # print(username)
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'myuser/register.html', locals())
                # print(email)
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'myuser/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                # print('hrer')
                new_user = models.User.objects.create(
                    name=username,
                    password=hash_code(password1),  # 使用加密密码
                    email=email,
                    sex=sex
                )

                # print(new_user.email, new_user.sex, new_user.name)
                new_user.save()
                message = ""  # 为空表示成功
                print('register success!')
                return redirect('/myuser/login/')  # 自动跳转到登录页面
    print('request is not POST')
    register_form = forms.RegisterForm()
    return render(request, 'myuser/register.html', locals())

def user_info(request):
    return render(request, 'myuser/home.html', locals())
