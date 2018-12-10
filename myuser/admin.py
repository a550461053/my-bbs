from django.contrib import admin

# Register your models here.
from . import models

# 注册模型

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'sex', 'c_time']


admin.site.register(models.User, UserAdmin)
