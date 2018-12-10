from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import InvalidPage, EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Count
# Create your views here.
from django.http import HttpResponse
from mybbs import models
from mybbs import forms


def home(request):
    return HttpResponse('hello!')

# 定义一个分页函数
def getPage(request, article_list):
    paginator = Paginator(article_list, 3)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
        print("-------------------")
        print(article_list)
        print("-----------------")
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


def hello(request):
    return render(request, 'hello.html')

def topic(request):
    if request.method == 'GET':
        topic_lists = models.Topic.objects.all()
        topic_list = [t.name for t in topic_lists]
        print(topic_list)
        # topic_list = ["话题1", "话题2", "话题3"]
        # context = {
        #     'topic_list': topic_list
        # }
        save_done = 'False'
        create_topic = "False"
        if len(topic_list) > 0:
            save_done = 'True'
        topic_form = forms.TopicForm()
        return render(request, 'mybbs/topic.html', locals())

    elif request.method == "POST":
        # if request.POST.get('submit') == "create_topic":
        #     create_topic = "True"
        #     print('create_topic = True')
        #     return redirect('/myuser/index', locals())
        #     return render(request, 'mybbs/topic.html', locals())
        topic_form = forms.TopicForm(request.POST)
        message = "请检查填写的内容！"
        if topic_form.is_valid():  # 获取数据
            topic_name = topic_form.cleaned_data['name']
            brief = topic_form.cleaned_data['brief']
            # admins = ','.join(topic_form.cleaned_data['admins'])  # 或者：request.POST.getlist('admins')
            sex = topic_form.cleaned_data['sex']
            same_topic_name = models.Topic.objects.filter(name=topic_name)
            if same_topic_name:  # 用户名唯一
                message = '主题已经存在，请重新选择主题名！'
                return render(request, 'mybbs/topic.html', locals())

            # 当一切都OK的情况下，创建新用户
            new_topic = models.Topic.objects.create(
                name=topic_name,
                brief=brief,
                # admins=admins,
                sex=sex
            )

            new_topic.save()
            save_done = 'True'
            create_topic = "False"
            # 更新列表
            topic_lists = models.Topic.objects.all()
            topic_list = [t.name for t in topic_lists]
            return render(request, 'mybbs/topic.html', locals())
        save_done = 'False'
        topic_form = forms.TopicForm(request.POST)
        # 更新列表
        topic_lists = models.Topic.objects.all()
        topic_list = [t.name for t in topic_lists]
        return render(request, 'mybbs/topic.html', locals())
    else:
        return HttpResponse("你所访问的页面不存在", status=404)
        # topic_form = forms.TopicForm(request.POST)
        # return render(request, 'mybbs/topic.html', locals())



def archive(request):
    try:
        # 先获取用户提交的year和month信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        # 通过filter过滤出对应年份的数据（icontains是包含）
        article_list = getPage(request, models.Article.objects.filter(date_publish__icontains=year + '-' + month))
    except Exception as e:
        # logging.error(e)
        print(e)
    return render(request, 'mybbs/archive.html', locals())

def biaoqian(request):
    try:
        # 获取请求的tag参数
        tag_name = request.GET.get('tag', None)
        # 找到tag所对应的Tag对象
        tag_obj = models.Tag.objects.get(name=tag_name)
        # 使用_set通过一对多关系进行查找
        article_list = getPage(request, tag_obj.article_set.all())
    except Exception as e:
        # logging.error(e)
        print(e)
    return render(request, 'mybbs/biaoqian.html', locals())

# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = models.Article.objects.get(pk=id)

            # 获取评论信息
            comments = models.Comment.objects.filter(article=article).order_by('id')
            comment_list = []
            for comment in comments:
                for item in comment_list:
                    if not hasattr(item, 'children_comment'):
                        setattr(item, 'children_comment', [])
                    if comment.pid == item:
                        item.children_comment.append(comment)
                        break
                if comment.pid is None:
                    comment_list.append(comment)

            # 评论表单
            comment_form = forms.CommentForm({'author': request.user.username,
                                        'email': request.user.email,
                                        'url': request.user.url,
                                        'article': id} if request.user.is_authenticated() else{'article': id})
        except models.Article.DoesNotExist:
            return render(request, 'mybbs/failure.html', {'reason': '没有找到对应的文章'})
    except Exception as e:
        # logging.error(e)
        print(e)
    return render(request, 'mybbs/article.html', locals())

def article_post(request):
    """
    评论表单
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        comment_form = forms.CommentForm({"author": request.user.name,
                                      "email": request.user.email,
                                      "url": request.user.url,
                                      "article": id} if request.user.is_authenticated() else {"article": id})
    return render(request, "mybbs/article_form.html", locals())




#############

# 文章详情
def article_list(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = models.Article.objects.get(pk=id)

            # 获取评论信息
            comments = models.Comment.objects.filter(article=article).order_by('id')
            comment_list = []
            for comment in comments:
                for item in comment_list:
                    if not hasattr(item, 'children_comment'):
                        setattr(item, 'children_comment', [])
                    if comment.pid == item:
                        item.children_comment.append(comment)
                        break
                if comment.pid is None:
                    comment_list.append(comment)

            # 评论表单
            comment_form = forms.CommentForm({'author': request.user.username,
                                        'email': request.user.email,
                                        'url': request.user.url,
                                        'article': id} if request.user.is_authenticated() else{'article': id})
        except models.Article.DoesNotExist:
            return render(request, 'mybbs/failure.html', {'reason': '没有找到对应的文章'})
    except Exception as e:
        #logging.error(e)
        print(e)
    return render(request, 'mybbs/article_list.html', locals())


# 提交评论
def comment_post(request):
    try:
        #获取表单内填入的内容
        comment_form = forms.CommentForm(request.POST)
        #进行验证的第一个表单验证
        if comment_form.is_vaild():
            #获取表单信息
            #cleaned_data()用来把接收到的文字清洗为符合django的字符
            #create是一个在一步操作中同时创建对象并且保存的便捷方法。
            comment = models.Comment.objects.create(username=comment_form.cleaned_data["author"],
                eamil=comment_form.cleaned_data["email"],
                url=comment_form.cleaned_data["url"],
                content=comment_form.cleaned_data["comment"],
                article_id=comment_form.cleaned_data["article"],
                #如果用户已经登录，则获取已经登录的用户，非登录用户将返回None
                #此处用的if语句有些特殊。
                user=request.user if request.user.is_authenticated() else None)
            comment.save()  #保存实例
        else:
            return render(request, "mybbs/failure.html", {"reason":comment_form.erros})
    except Exception as e:
        # logger.error(e)
        pass
        #重定向到进来之前的网页
        #HTTP_REFERER是http的头文件的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer,告诉服务器我是从哪个页面链接过来的，服务器借此获得一些信息用于处理。
    return redirect(request.META['HTTP_REFERER'])