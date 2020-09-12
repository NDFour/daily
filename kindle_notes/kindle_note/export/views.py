from django.shortcuts import render
from django.http import HttpResponse
import time

from .forms import UploadForm

from .tasks import add
from .tasks import export_user_db


# 自定义 保存文件 的方法
def save_file(file, file_name, mail_addr, message):
    folder_name = 'user_uploaded/'
    f_name = str(time.time()).replace('.', '_') + '.db'

    with open(folder_name + f_name, 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    # 使用 celery 执行 异步任务
    # add.delay(5,12.3)
    export_user_db.delay( folder_name + f_name , mail_addr, message)



# Create your views here.
def index(request):
    if request.method == 'POST':
        # my_form 包含提交的数据
        my_form = UploadForm(request.POST, request.FILES)
        # my_form = UploadForm(request.POST)

        if my_form.is_valid():
            # return HttpResponse('post 请求 保存文件成功')

            # mail_addr:
            mail_addr = request.POST.get('mail_addr', '')
            # message:
            message = request.POST.get('message', '')
            # my_file:
            save_file(
                request.FILES['my_file'],
                '默认',
                mail_addr, message
                )

            context = {
                'status': 0,
                'title': '恭喜，文件上传成功！',
                'msg': '文件上传成功，请耐心等待片刻，您的邮箱即可收到 我们发出的邮件，内含导出的生词本可直接下载。'
            }
            return render(request, 'export/export_show_msg.html', context)
        else:
            # return HttpResponse('文件上传错误，请重新尝试或联系管理员。')
            context = {
                'status': -1,
                'title': 'Sorry，文件上传失败了',
                'msg': '文件上传错误，请重新尝试或联系管理员。管理员微信：ndfour'
            }
            return render(request, 'export/export_show_msg.html', context)

        context = {
            'status': -2,
            'title': 'Sorry，文件上传失败了',
            'msg': '表单数据不合法，请重新尝试或联系管理员。管理员微信：ndfour'
        }
        return render(request, 'export/export_show_msg.html', context)

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

