# 基于Django开发的bbs网站

## 安装运行
git clone git@github.com:a550461053/my-bbs.git
cd my-bbs/
pip install -rU requirements.txt
python manager.py runserver 
打开http://127.0.0.1:8000/myuser/index

## 界面介绍
系统主页：http://127.0.0.1:8000/index
用户主页：http://127.0.0.1:8000/myuser/index
文章主页：http://127.0.0.1:8000/mybbs/index


## 简介
Django是一个web框架，框架的作用就是处理request和reponse。
至于Djnago所提供的是一个开发服务器，这个开发服务器，没有经过安全测试，而且使用的是python自带的simple HTTPServer创建的，在安全性和效率上都是不行的。

我们需要开发一个电商网站，那么产品列表、购物车、下单等等这都是不同的业务线，我们可以把每条业务线都看做一个App

Django和Apache的区别
- Django的自带服务器作为服务启动，一个错误就会宕掉整个服务
- Apache和eginx都只是挂个wsgi的线程。
- 安全性/性能/HA等



## Django项目的开发流程

0. 创建项目
django-admin startproject mydjango

- 产生结构
mydjango/
    manage.py
    mydjango/
        __init__.py
        settings.py
        urls.py
        wsgi.py

- 解释
	+ 最外层的:file: mydjango/ 根目录只是你项目的容器。
	+ manage.py: 一个让你用各种方式管理 Django 项目的命令行工具。
	+ 里面一层的 mydjango/ 目录包含你的项目，它是一个纯 Python 包。
	+ mydjango/__init__.py：一个空文件，告诉 Python 这个目录应该被认为是一个 Python 包。
	+ mydjango/settings.py：Django 项目的配置文件。
	+ mydjango/urls.py：Django 项目的 URL 声明，就像你网站的“目录”。
	+ mydjango/wsgi.py：作为你的项目的运行在 WSGI 兼容的Web服务器上的入口。


1. 创建app
python manage.py startapp mybbs
产生：
- migrations/：存储一些文件以跟踪你在models.py文件中创建的变更，用来保持数据库和models.py的同步。 
- admin.py：django内置的应用程序Django Admin的配置文件。 
- apps.py：应用程序本身的配置文件。 
- models.py：这里是我们定义Web应用程序数据实例的地方。models会由Django自动转换为数据库表。 
- tests.py：这个文件用来写当前应用程序的单元测试。 
- views.py：这是我们处理Web应用程序请求(request)/响应(resopnse)周期的文件。

2. 安装app

编辑setting.py，添加INSTALLED_APPS = ['mybbs',]
Django默认安装了6个内置应用程序，提供大多数web应用所需的常用功能，如身份验证、会话、静态文件管理等

3. 编写视图view
视图是接收httprequest对象，并返回一个httpresponse对象的python函数。
vi views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse('hello!')


4. 定义url
通过正则匹配请求的url
vi urls.py

from django.contrib import admin
from django.urls import path

from mybbs import views

urlpatterns - [
    path('^$', views.home, name='home')  # 主页
    path('admin/', admin.site.urls),
]

也可以通过在mybbs下面创建一个urls.py模块
然后根URL指定include该模块即可。

5. 更新数据库
python manage.py makemigrations mybbs
python manage.py migrate
6. 创建管理员
忘记密码，直接新建一次就行
python manage.py createsuperuser
7. 如果数据库有问题
重新删除数据库，删除migrations，重新runserver即可重新建立sqlite数据库
