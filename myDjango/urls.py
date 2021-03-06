"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from mybbs import views as mybbs_views

urlpatterns = [
    path('', mybbs_views.home),  # ^$
    path('home/', mybbs_views.home),
    path('admin/', admin.site.urls),
    # path('mybbs/', include('mybbs.urls')),
    # path('myuser/', include('myuser.urls')),
    path('mybbs/', include('mybbs.urls'), name='mybbs'),
    path('myuser/', include('myuser.urls'), name='myuser'),
    # path('mybbs/', include(('mybbs.urls', 'mybbs'), namespace='mybbs')),
    # path('myuser/', include(('myuser.urls', 'myuser'), namespace='myuser')),

    path('captcha/', include('captcha.urls')),
]
