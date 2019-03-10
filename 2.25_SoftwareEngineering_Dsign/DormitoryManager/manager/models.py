from django.db import models

# Create your models here.
class Student(models.Model):
    number = models.IntegerField('学号', blank=False)
    name = models.CharField('姓名', max_length=255)
    classNum = models.IntegerField('班级', blank=False)
    gender = models.IntegerField('性别', blank=False)
    dromitory = models.IntegerField('宿舍', blank=False, default=111)
    bed = models.IntegerField('床位', blank=False, default=1)

    def __str__(self):
        return self.name

class Dormitory(models.Model):
    number = models.IntegerField('宿舍号', blank=False)
    stu_1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stu_1', blank=True)
    stu_2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stu_2', blank=True)
    stu_3 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stu_3', blank=True)
    stu_4 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stu_4', blank=True)
    star = models.IntegerField('内务评级')
    info = models.CharField('简介', max_length=255)
    gender = models.IntegerField('类别（男/女）', blank=False)
    waterFee = models.IntegerField('水费', blank=True, default=0)
    elecFee = models.IntegerField('电费', blank=True, default=0)
    isRepair = models.IntegerField('报修', blank=False, default=0)

    def __str__(self):
        return str(self.number)