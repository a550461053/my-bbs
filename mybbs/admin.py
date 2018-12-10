from django.contrib import admin

# Register your models here.
from . import models
from myuser.models import User

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_recommend', 'click_count']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'brief', 'sex', 'c_time']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'index']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
