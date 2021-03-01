"""untitled URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html$', views.Login.as_view()), # 类名的关联方法
    url(r'^logout.html$', views.logout),
    url(r'^index.html$', views.index),

    url(r'^classes.html$', views.handle_classes),
    url(r'^add_classes.html$', views.handle_add_classes),
    url(r'^edit_classes.html$', views.handle_edit_classes),

    url(r'^student.html$', views.handle_student),
    url(r'^add_student.html$', views.add_student),
    url(r'^edit_student.html$', views.edit_student),

    url(r'^teacher.html$', views.handle_teacher),
    url(r'^add_teacher.html$', views.add_teacher),
    url(r'^edit_teacher-(\d+).html$', views.edit_teacher),
    # 左右移动编辑
    url(r'^edit_teacher_lr-(\d+).html$', views.edit_teacher_lr),

    # 三级菜单
    url(r'^menu.html$', views.menu),
    url(r'^fetch_city.html$', views.fetch_city),
    url(r'^fetch_xian.html$', views.fetch_xian),

    # 测试数据库
    url(r'^test.html$', views.test),

    # 文件上传
    url(r'^upload_form.html$', views.upload_form),
    url(r'^upload_ajax.html$', views.upload_ajax),

    # jsonp
    url(r'^jsonp.html$', views.test_jsonp),
]
