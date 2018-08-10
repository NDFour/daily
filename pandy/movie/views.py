from django.shortcuts import render
from .models import Movie
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('-v_pub_date')[:10]
    context = {
            'movie_list': movie_list,
            }
    return render(request, 'movie/index.html', context)


def movie_search(request, movie_name):
    movie_list = Movie.objects.filter(v_name__icontains=movie_name)[:100]
    context = {
            'movie_list': movie_list,
            }
    return render(request, 'movie/index.html', context)
    # return HttpResponse('search page %s' % movie_name)
    

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id  = movie_id)
    # 阅读量自增 1 
    movie.increase_views()

    return render(request, 'movie/detail.html', {'movie': movie})


def confirm_invalid(request, movie_id, urlstate):
    context = {
            'movie_id': movie_id,
            'urlstate': urlstate,
            }
    return render(request, 'movie/confirm_invalid.html', context)


def invalid_url_report(request, movie_id, urlstate):
    info=''
    if urlstate == 1:
        # 验证数据库 网盘有效 标志位是否为不可用
        movie = get_object_or_404(Movie, id = movie_id)
        urlstate = movie.v_valid

        # 还未有人报告过还 失效链接
        if urlstate == 1:
            # 置 v_valid 位为0
            movie.v_valid=0
            movie.save()
            mail_message='网盘地址失效通知\n\nID:%s\n名字:%s'%(movie.id, movie.v_name)
            mail_subject='tnt1024 网盘链接失效通知 %s' % movie.id
            # send email 
            send_mail(mail_subject, mail_message, 'lgang219@qq.com', ['ndfour@foxmail.com'], fail_silently=True)

        # 已有人报告过该 失效链接
        else:
            info='管理员正在努力重新补链接中...'
    else:
        info='管理员正在努力重新补链接中...'

    return render(request, 'movie/invalid_url_report.html', {'urlstate': urlstate,'info': info})
