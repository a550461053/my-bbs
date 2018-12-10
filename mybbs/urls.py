# coding=utf-8

# @Time    : 2018-11-22 19:38
# @Auther  : Batista-yu
# @Contact : 550461053@gmail.com
# @license : (C) Copyright2016-2018, Batista Yu Limited.

'''

'''

from django.urls import path

from . import views

app_name = 'mybbs'

urlpatterns = [
    path('', views.home, name='index'),
    path('hello/', views.hello),
    path('topic/', views.topic),
    path('comment/post/', views.comment_post, name='comment_post'),
    path('article/', views.article_list),
    path('article/form/', views.article_post),
]

