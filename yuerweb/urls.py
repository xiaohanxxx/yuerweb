"""yuerweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
from yuerweb import views
import notifications.urls
import notifications
from django.views.generic.base import RedirectView
from webmanage import views as manageviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),

    url(r'luntan/', include('luntan.urls')),

    url(r'hospital/', include('hospital.urls')),
    url(r'shiguanbaby/', include('shiguanbaby.urls')),
    url(r'taolun/', include('taolun.urls')),

    url(r'baike/', include('baike.urls')),
    url(r'users/', include('users.urls')),
    url(r'webmanage/', include('webmanage.urls')),

    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),  # 富文本路由
    path('notifications/', include(notifications.urls, namespace='notifications')),

    path('search/', include('haystack.urls')),
    # url(r'^upload', views.upload)  # 测试路由

    # 移动端路由
    path('index', views.m_index),
    path('m_login', views.m_login),
    path('m_zhuce', views.m_zhuce),
    path('m_forget', views.m_forget)
]
