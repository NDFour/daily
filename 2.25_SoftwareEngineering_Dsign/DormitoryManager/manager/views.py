from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Student, Dormitory

# Create your views here.
def index(request):
    # return HttpResponse("Hello,world. You're at the manager index.")
    dormitoryList = Dormitory.objects.all().order_by('number')
    stuList = Student.objects.all().order_by('number')
    starList = Dormitory.objects.all().order_by("-star")
    context = {
            'dormitoryList': dormitoryList,
            'stuList': stuList,
            'dorSize': "hello",
            'stuSize': len(stuList),
            'starList': starList,
            }
    return render(request, 'index.html', context)

# 宿舍详情页
def dormitory_detail(request, dormitory_number):
    dormitory = get_object_or_404(Dormitory, number = dormitory_number)
    starList = Dormitory.objects.all().order_by("-star")
    context = {
        'dormitory': dormitory,
        'starList': starList,
        }
    return render(request, 'index_Dormitory.html', context)

# 学生详情页
def student_detail(request, stu_number):
    student = get_object_or_404(Student, number = stu_number)
    starList = Dormitory.objects.all().order_by("-star")
    context = {
        'student': student,
        'starList': starList,
        }
    return render(request, 'index_Student.html', context)

# 宿舍保修
def repair(request, dormitory_number):
    dormitory = get_object_or_404(Dormitory, number = dormitory_number)
    try:
        dormitory.isRepair = 1
        dormitory.save()
        return HttpResponse('报修成功' + str(dormitory.isRepair))
    except:
        return HttpResponse('报修失败')
