from django.db import models


from myuser.models import *

# Create your models here.
class Topic(models.Model):
    """
    话题
    """
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = models.CharField(max_length=128, unique=True)
    # image = models.ImageField()
    brief = models.CharField(null=True,blank=True,max_length=255)
    # 一般页面的版块是固定死的，但是我们想动态生成版块的时候，我们需要定义一个位置字段和是否显示字段
    # 一般常规的网站首页都是固定的
    # set_as_top_menu = models.BooleanField(default=False)
    # position_index = models.SmallIntegerField()
    # 可以有多个管理员
    # admins = models.ManyToManyField("myuser.User", blank=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    class Meta:
        """
        元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
       """
        ordering = ['c_time']
        verbose_name = '话题'
        verbose_name_plural = verbose_name


# 分类(category)模型
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name

# 标签(tag)模型
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 自定义一个文章Model的管理器
# 1、新加一个数据处理的方法(本次使用)
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y年%m月文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

class Article(models.Model):
    """
    文章
    """

    status_choices = (('draft', u"草稿"),
                      ('published', u"已发布"),
                      ('hidden', u"隐藏"),
                      )

    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    status = models.CharField(max_length=128, verbose_name="发表状态",
                              choices=status_choices,
                              default="draft")
    user = models.ForeignKey('myuser.User', verbose_name='用户', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    objects = ArticleManager()
    is_deleted = models.BooleanField(verbose_name="已删除", default=False, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)

    # 文章置顶功能
    priority = models.IntegerField(u"优先级", default=1000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def delete(self, using=None, keep_parents=False):
        # 自定义删除，软删除，保留数据，只是设置标志位。
        self.is_deleted = True
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.title.capitalize()  # 首字母大写
        return super().save(force_insert=force_insert, force_update=force_update,
                            using=using, update_fields=update_fields)


class Comment(models.Model):
    """
    评论
    """
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    user = models.ForeignKey('myuser.User', blank=True, null=True, verbose_name='用户', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章', on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论', on_delete=models.CASCADE)

    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        """
        元数据里定义用户按创建时间的反序排列，也就是最近的最先显示；
       """
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


