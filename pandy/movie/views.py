from django.shortcuts import render
from .models import Movie, Passwds
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

import requests
import re

# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('-v_pub_date')[:10]
    context = {
            'movie_list': movie_list,
            'page_title': '',
            }
    return render(request, 'movie/index.html', context)


def movie_search(request, movie_name):
    movie_list = Movie.objects.filter(v_name__icontains=movie_name)[:100]

    # 是否展示支付宝 领红包 js代码
    alipay_code = '0'
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie_list': movie_list,
            'movie_name': movie_name,
            'page_title': movie_name+' 搜索结果',
            'alipay_code': alipay_code,
            }
    return render(request, 'movie/index.html', context)
    # return HttpResponse('search page %s' % movie_name)

# 热搜榜，根据访问量返回阅读量最高的20部电影
def movie_resou(request):
    movie_list = Movie.objects.order_by('-v_views')[:20]
    context = {
            'movie_list': movie_list,
            'page_title': '近期热搜榜',
            }
    return render(request, 'movie/index.html', context)
    

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id  = movie_id)
    # 阅读量自增 1 
    movie.increase_views()

    # 是否展示支付宝 领红包 js代码
    alipay_code = "0"
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie': movie,
            'alipay_code': alipay_code,
            }

    return render(request, 'movie/detail.html', context)


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

        # 判断网盘链接是否确实已失效
        if isInvalid(movie.v_bdpan) == 1:
            # 置 v_valid 位为0
            movie.v_valid=0
            movie.save()
            mail_message='网盘地址失效通知\n\nID:%s\n名字:%s\n\n网盘地址:%s\n网盘密码:%s\n采集页链接:%s\n\n链接仍旧有效？\nhttp://tnt1024.com/movie/reset_form/%s'%(movie.id, movie.v_name, movie.v_bdpan, movie.v_pass, movie.v_href, movie.id)
            mail_subject='tnt1024 网盘链接失效通知 %s' % movie.id
            # send email 
            send_mail(mail_subject, mail_message, 'lgang219@qq.com', ['ndfour@foxmail.com'], fail_silently=True)

        # 经程序判断网盘链接未失效
        else:
            # 程序判断链接未失效
            info='[CODE:8001] 管理员正在努力重新补链接中...'

    # 已有人报告过该失效链接
    else:
        info='[CODE:8002] 管理员正在努力重新补链接中...'

    return render(request, 'movie/invalid_url_report.html', {'urlstate': urlstate,'info': info})

def reset_form(request, movie_id):
    msg = '修改 %s 网盘状态' %movie_id 
    context = {
            'msg': msg,
            'page_title': '修改资源网盘状态',
            'movie_id': movie_id,
            }
    return  render(request, 'movie/reset_valid.html', context)

def reset_valid(request):
    movie_id = request.GET['movie_id']
    passwd = request.GET['b']
    movie_id = int(movie_id)

    # 根据后台设置的密码标识符，获取到对应的密码记录
    passwd_obj = get_object_or_404(Passwds, p_code=1001)

    msg = '重置 %s 的网盘状态' %str(movie_id)
    if passwd == passwd_obj.p_value:
        try:
            movie = get_object_or_404(Movie, id = movie_id)
            movie.v_valid = 1
            movie.save()
            msg+='成功'
        except:
            msg+='失败，获取资源对象出错'
    else:
        msg+='%s-%s失败，验证码出错'%(passwd, passwd_obj.p_value)

    context = {
            'msg' : msg,
            'page_title': '重置影片网盘状态',
            'movie_id': movie_id,
            }
    return render(request, 'movie/reset_valid.html', context)


##################### 以下函数与渲染网页无关

def getHtml(url):
    headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'pan.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
    r=requests.get(url,headers=headers)
    r.encoding = r.apparent_encoding
    return r.text

# 判断网盘链接是否真的失效
def isInvalid(url):
    html_text = getHtml(url)
    answer = re.search('不存在', html_text)
    # 失效
    if(answer):
        return 1
    # 未失效
    else:
        return 0

