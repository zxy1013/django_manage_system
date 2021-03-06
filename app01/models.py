from django.db import models
# python manage.py makemigrations
# python manage.py migrate

class Classes(models.Model):
    caption = models.CharField(max_length=32)

class Student(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ForeignKey('Classes',on_delete=models.CASCADE)

class Teacher(models.Model):
    name = models.CharField(max_length=32)
    cls = models.ManyToManyField('Classes')

class Administrator(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


# 三级联动表
class Province(models.Model):
    name = models.CharField(max_length=32)

class City(models.Model):
    name = models.CharField(max_length=32)
    pro = models.ForeignKey("Province",on_delete=models.CASCADE)

class Xian(models.Model):
    name = models.CharField(max_length=32)
    cy = models.ForeignKey("City",on_delete=models.CASCADE)

# 数据库复习创建表
class Book(models.Model):
    name =models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=32)
    m = models.ManyToManyField('Book')
    def __str__(self):
        return self.name

# 文件上传
class Img(models.Model):
    path = models.CharField(max_length=128)