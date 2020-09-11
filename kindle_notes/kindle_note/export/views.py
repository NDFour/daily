from django.shortcuts import render
from django.http import HttpResponse
import time

from .forms import UploadForm


# 自定义 保存文件 的方法
def save_file(file):
    folder_name = 'user_uploaded/'
    f_name = str(time.time()).replace('.', '_') + '.db'

    with open(folder_name + f_name, 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)



# Create your views here.
def index(request):
    if request.method == 'POST':
        # my_form 包含提交的数据
        my_form = UploadForm(request.POST, request.FILES)

        if my_form.is_valid():
            # return HttpResponse('post 请求 保存文件成功')
            save_file(request.FILES['my_file'])
            context = {
                'status': 0,
                'title': '恭喜，文件上传成功！',
                'msg': '文件上传成功，请耐心等待管理员操作。'
            }
            return render(request, 'export/export_show_msg.html', context)
        else:
            # return HttpResponse('文件上传错误，请重新尝试或联系管理员。')
            context = {
                'status': -1,
                'title': 'Sorry，文件上传失败了',
                'msg': '文件上传错误，请重新尝试或联系管理员。'
            }
            return render(request, 'export/export_show_msg.html', context)

        return HttpResponse('post 请求 文件不合法')

    elif request.method == 'GET':
        my_form = UploadForm()

        context = {
            'form': my_form,
        }

        # return HttpResponse('Welcome to export app') 
        return render(request, 'export/export_index.html', context)



# 点击文件上传按钮后信息展示页
'''
def upload_msg(request):
    return HttpResponse('文件上传展示页')
'''

