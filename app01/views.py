from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from django import views
import json
from util.page import PagerHelper
import os

class Login(views.View):

    def get(self,request, *args, **kwargs):
        return render(request, 'login.html', {'msg': ''})

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=user, password=pwd).count()
        if c:
            request.session['is_login'] = True
            request.session['username'] = user
            rep = redirect('/index.html')
            return rep
        else:
            message = "用户名或密码错误"
            return render(request, 'login.html', {'msg': message})


def logout(request):
    request.session.clear()
    return redirect('/login.html')


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login.html')
    return inner


@auth
def index(request):
    current_user = request.session.get('username')
    return render(request, 'index.html',{'username': current_user})




@auth
def handle_classes(request):
    if request.method == "GET":
        current_user = request.session.get('username')
        # 添加数据
        # for i in range(100):
        #     models.Classes.objects.create(caption='160%s'%str(i))
        # models.Classes.objects.create(caption='二班')
        # models.Classes.objects.create(caption='三班')
        # 当前页
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        # 所有数据的个数
        total_count = models.Classes.objects.all().count( )
        # 调用分页函数 最后一个参数为每页个数
        obj = PagerHelper(total_count, current_page, '/classes.html', 10)
        pager = obj.pager_str( )
        cls_list = models.Classes.objects.all()[obj.db_start:obj.db_end]
        return render(request, 'classes.html', {'username': current_user, 'cls_list': cls_list, 'str_pager': pager})

    elif request.method == "POST":
        # # Form表单提交的处理方式，页面会刷新。
        # caption = request.POST.get('caption', None)
        # if caption:
        #     models.Classes.objects.create(caption=caption)
        #     return redirect('/classes.html')

        # Ajax表单提交的处理方式 推荐使用
        response_dict = {'status': True, 'error': None, 'data': None}
        caption1 = request.POST.get('caption', None)
        # Ajax表单提交的处理方式 type表示为添加还是修改删除
        if int(request.POST.get('type_op'))==1:
            if caption1:
                obj = models.Classes.objects.create(caption=caption1)
                # 将存入数据库的id存入数据中
                response_dict['data'] = {'id': obj.id, 'caption': obj.caption}
            else:
                response_dict['status'] = False
                response_dict['error'] = "标题不能为空"

        elif int(request.POST.get('type_op'))==2:
            nid = request.POST.get('id')
            models.Classes.objects.filter(id=nid).update(caption=caption1)
        elif int(request.POST.get('type_op')) == 3:
            nid = request.POST.get('id')
            models.Classes.objects.filter(id=nid).delete()

        # 字典转换为字符串
        return HttpResponse(json.dumps(response_dict))


@auth
def handle_add_classes(request):
    message = ""
    if request.method == "GET":
        return render(request, 'add_classes.html', {'msg': message})
    elif request.method == "POST":
        caption = request.POST.get('caption',None)
        if caption:
            models.Classes.objects.create(caption=caption)
        else:
            message = "标题不能为空"
            return render(request, 'add_classes.html', {'msg': message})
        return redirect('/classes.html')
    # 此时不支持其他方式的请求
    else:
        return redirect('/index.html')


@auth
def handle_edit_classes(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        obj = models.Classes.objects.filter(id=nid).first()
        # 编辑框显示
        return render(request, 'edit_classes.html', {'obj': obj})
    elif request.method == "POST":
        nid = request.POST.get('nid')
        caption = request.POST.get('caption')
        models.Classes.objects.filter(id=nid).update(caption=caption)
        return redirect('/classes.html')
    else:
        return redirect('/index.html')




@auth
def handle_student(request):
    if request.method == "GET":
        # # 添加数据
        # for i in range(9,18):
        #     models.Student.objects.create(name='root' + str(i),
        #                                   cls_id=str(i))
        result = models.Student.objects.all()
        current_user = request.session.get('username')
        return render(request, 'student.html', {'username': current_user,'result': result})
    else:
        return redirect('/index.html')


@auth
def add_student(request):
    if request.method == "GET":
        cls_list = models.Classes.objects.all()
        return render(request, 'add_student.html', {'cls_list': cls_list})
    elif request.method == "POST":
        name = request.POST.get('name')
        cls_id = request.POST.get('cls_id')
        models.Student.objects.create(name=name,cls_id=cls_id)
        return redirect('/student.html')


@auth
def edit_student(request):
    if request.method == "GET":
        cls_list = models.Classes.objects.all()
        nid = request.GET.get('nid')
        obj = models.Student.objects.get(id=nid)
        return render(request, 'edit_student.html', {'cls_list': cls_list, "obj": obj})
    elif request.method == "POST":
        nid = request.POST.get('id')
        name = request.POST.get('name')
        cls_id = request.POST.get('cls_id')
        models.Student.objects.filter(id=nid).update(name=name,cls_id=cls_id)
        return redirect('/student.html')




@auth
def handle_teacher(request):
    if request.method == "GET":
        current_user = request.session.get('username')
        # # 循环次数较多
        # teacher_list = models.Teacher.objects.all()
        # # for obj in teacher_list:
        # #     print(obj.cls.all().values('caption'))
        # return render(request, 'teacher.html', {'username': current_user, 'teacher_list': teacher_list})

        # 后台传送字典 将教授多门班级的老师只显示一次 循环次数较少
        # id__in=models.Teacher.objects.all()[0:3] 显示前三个老师
        teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.all()).values('id','name','cls__id','cls__caption')
        result = {}
        for t in teacher_list:
            if t['id'] in result:
                if t['cls__id']:
                    result[t['id']]['cls_list'].append({'id':t['cls__id'], 'caption': t['cls__caption'] })
            else:
                if t['cls__id']:
                    temp = [{'id': t['cls__id'], 'caption': t['cls__caption']},]
                else:
                    temp = []
                result[t['id']] = {
                    'nid': t['id'],
                    'name': t['name'],
                    'cls_list': temp
                }
        return render(request, 'teacher.html', {'username': current_user, "teacher_list": result})
    else:
        return redirect('/index.html')


@auth
def add_teacher(request):
    if request.method == 'GET':
        cls_list = models.Classes.objects.all()
        return render(request, 'add_teacher.html', {'cls_list': cls_list})
    elif request.method == "POST":
        name = request.POST.get('name')
        cls = request.POST.getlist('cls')
        # 创建老师
        obj = models.Teacher.objects.create(name=name)
        # 创建老师和班级的对应关系
        obj.cls.add(*cls)
        return redirect('/teacher.html')
    else:
        return redirect('/index.html')


@auth
def edit_teacher(request,nid):
    # 获取当前老师信息
    # 获取当前老师对应的所有班级
    # 获取当前老师未对应的所有班级
    if request.method == "GET":
        obj = models.Teacher.objects.get(id=nid)
        obj_cls_list = obj.cls.all().values_list('id')
        # <QuerySet [(10,), (11,)]>
        id_list = list(zip(*obj_cls_list))[0]if obj_cls_list else [ ]
        # zip将每列分开放在一起 (10, 11)
        cls_list = models.Classes.objects.all()
        return render(request, 'edit_teacher.html', {'obj': obj, "cls_list": cls_list, "id_list": id_list})
    elif request.method == "POST":
        name = request.POST.get('name')
        cls_li = request.POST.getlist('cls')
        obj = models.Teacher.objects.get(id=nid)
        obj.name = name
        obj.save()
        obj.cls.set(cls_li)
        return redirect('/teacher.html')
    else:
        return redirect('/index.html')


# 左右移动编辑
@auth
def edit_teacher_lr(request,nid):
    # 获取当前老师信息
    # 获取当前老师对应的所有班级
    # 获取当前老师未对应的所有班级
    if request.method == "GET":
        obj = models.Teacher.objects.get(id=nid)
        # 获取当前老师已经管理的所有班级
        obj_cls_list = obj.cls.all( ).values_list('id', 'caption')
        # 已经管理的班级的ID列表
        id_list = list(zip(*obj_cls_list))[ 0 ] if obj_cls_list else [ ]
        # 获取不包括已经管理的班级，
        cls_list = models.Classes.objects.exclude(id__in=id_list)
        return render(request, 'edit_teacher_lr.html', {'obj': obj,
                                                     'obj_cls_list': obj_cls_list,
                                                     "cls_list": cls_list,
                                                     "id_list": id_list
                                                     })
    elif request.method == "POST":
        name = request.POST.get('name')
        cls_li = request.POST.getlist('cls')
        obj = models.Teacher.objects.get(id=nid)
        obj.name = name
        obj.save( )
        obj.cls.set(cls_li)
        return redirect('/teacher.html')
    else:
        return redirect('/index.html')




# 三级菜单
def menu(request):
    # # 创建数据
    # for i in range(10):
    #     models.Province.objects.create(name="河北"+str(i))
    # for i in range(5):
    # # 关联外键，id = 1
    #     models.City.objects.create(name="廊坊" + str(i),pro_id=1)
    pro_list = models.Province.objects.all()
    return render(request, 'menus.html', {"pro_list": pro_list})


def fetch_city(request):
    # 根据用户传入的省份ID，获取与其相关的所有市ID
    province_id = request.GET.get('province_id')
    result = models.City.objects.filter(pro_id=province_id).values('id','name')
    # result = models.City.objects.filter(pro_id=province_id).values_list('id','name')

    # QuerySet内部放置对象
    result = list(result)
    data = json.dumps(result)
    return HttpResponse(data)


def fetch_xian(request):
    # # 创建数据
    # for i in range(10):
    #     models.Xian.objects.create(name='县'+ str(i), cy_id=1)
    city_id = request.GET.get('city_id')
    xian_list = models.Xian.objects.filter(cy_id=city_id).values('id','name')
    xian_list = list(xian_list)
    return HttpResponse(json.dumps(xian_list))




# 测试数据库
def test(request):
    # 单表查找
    pro_list = models.Province.objects.all()
    # name='河北0'
    models.Province.objects.filter(name='河北0')
    # name!='河北0'
    models.Province.objects.exclude(name='河北0')

    # 一对多 正向查找（具有外键字段）
    v = models.City.objects.all()[0]
    # print(v.pro.name)

    # 一对多 反向查找
    v = models.Province.objects.values('id','name','city__name')
    # 或
    pro_list = models.Province.objects.all()
    for item in pro_list:
        # id__in
        c = item.city_set.filter(id__lt=3).values("name")
        # print(item.name,c)


    # # 添加。由于不是外键，可以不设置m的值
    # models.Book.objects.create(name='书名')
    # models.Author.objects.create(name='人名')


    # 多对多正向查找
    obj = models.Author.objects.get(id=1)
    # print(obj.m.all())

    author_list = models.Author.objects.all()
    for author in author_list:
        a = author.m.all( )
        # print(author.name,a)

    author_list = models.Author.objects.values('id', 'name', 'm', "m__name")
    for item in author_list:
        item[ 'm__name' ]
        # print(item[ 'id' ], item[ 'name' ], item[ 'm__name' ])

    # 多对多反向查找 由书得到作者
    obj = models.Book.objects.get(id=1)
    obj.author_set.all()


    # 多对多添加
    obj = models.Author.objects.get(id=1)
    # 第三张表中增加一个对应关系
    # 此时book表中需要有id为5,6,7的。 正向
    obj.m.add(9)
    obj.m.add(10,11)
    # 删除
    obj.m.remove(5)
    obj.m.remove(7,6)
    # 清空
    obj.m.clear()
    # 更新obj对应的m和book的关系
    obj.m.set([5,10,9])

    # 反向操作 添加关系
    obj = models.Book.objects.get(id=1)
    obj.author_set.add(1)
    obj.author_set.add(7,2,3,4)

    return HttpResponse("OK")




# 文件上传 表单
def upload_form(request):
    if request.method == 'GET':
        img_list = models.Img.objects.all()
        return render(request, 'upload_form.html', {'img_list': img_list})
    elif request.method == "POST":
        # 拿文件内容
        obj = request.FILES.get('file_text')
        file_path = os.path.join('static','upload',obj.name)
        # html走的静态路径为abc
        file_path1 = os.path.join('abc', 'upload', obj.name)
        # file走的路径为static
        f = open(file_path, 'wb')
        # 分块存储
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        models.Img.objects.create(path=file_path1)
        return redirect('/upload_form.html')
    else:
        return redirect('/index.html')


# 文件上传 ajax
def upload_ajax(request):
    if request.method == 'GET':
        img_list = models.Img.objects.all()
        return render(request,'upload_ajax.html',{'img_list': img_list})
    elif request.method == "POST":
        obj = request.FILES.get('file_text')
        file_path = os.path.join('static','upload',obj.name)
        # html走的静态路径为abc
        file_path1 = os.path.join('abc', 'upload', obj.name)
        f = open(file_path, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        models.Img.objects.create(path=file_path1)
        ret = {'status': True, 'path': file_path1}
        # 传给iframe
        return HttpResponse(json.dumps(ret))

def test_jsonp(request):
    return render(request,'jsonp.html')