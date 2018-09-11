from .models import Movie, Passwds
from onlineplay.models import Onlineplay
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from django.urls import reverse

# 验证网盘链接是否失效
import requests
import re
import os
import traceback
import codecs
from django.views.decorators.cache import cache_page

# 分页
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def index(request):
    movie_list = Movie.objects.all().order_by('-v_pub_date')
    # 一页的数据数据
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取第一页的数据并返回
        movie_list = paginator.page(1)
    except:
        movie_list = paginator.page(1)

    resou_movie_list = Movie.objects.order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'movie_index', # 传递给模板，用以区别显示 页码 链接
            }
    return render(request, 'movie/index.html', context)

@cache_page(60 * 15)
def index_by_page(request, page_num):
    try:
        tmp = int(page_num)
    except:
        tmp = 1
    page_num = tmp

    # 一页的数据数目
    per_page = 12
    movie_list = Movie.objects.all().order_by('-v_pub_date')
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取当前页码中的数据记录
        movie_list = paginator.page(page_num)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页

    resou_movie_list = Movie.objects.order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'movie_index_by_page',
            }

    return render(request, 'movie/index.html', context)

# 正常通过 navbar 中的 Form 搜索
def movie_search_navbar(request):
    movie_name = request.GET['movie_name']

    # 搜索在线 或 搜索网盘
    search_type = ''
    try:
        search_type = request.GET['onlineplay_search']
    except:
        search_type = ''
    if search_type:
        pass
    else:
        try:
            search_type = request.GET['movie_search']
        except:
            search_type = ''

    # 尝试获取页码
    try:
        page_num = request.GET['page_num']
    except:
        page_num = 1

    # 根据不同的搜索按钮 (onlineplay_search, movie_search)，搜索不同的数据
    if search_type == 'onlineplay_search':
        movie_list = Onlineplay.objects.filter(v_name__icontains=movie_name)
    else:
        movie_list = Movie.objects.filter(v_name__icontains=movie_name)

    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator(movie_list, per_page)
    try:
        # 获取当前页码中的数据记录
        movie_list = paginator.page(page_num)
    except:
        movie_list = paginator.page(1)

    resou_movie_list = Movie.objects.order_by('-v_views')[:7]

    # 是否展示支付宝 领红包 js代码
    alipay_code = '0'
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'movie_name': movie_name,
            'page_title': movie_name+' 搜索结果',
            'alipay_code': alipay_code,
            'url_name': 'movie_search_navbar',
            'search_type': search_type,
            }
    return render(request, 'movie/index.html', context)
    # return HttpResponse('search page %s' % movie_name)

# 热搜榜，根据访问量返回阅读量最高的20部电影
@cache_page(60 * 15)
def movie_resou(request):
    movie_list = Movie.objects.order_by('-v_views')[:20]
    # 热搜页 一页的 电影数量
    per_page = 20
    paginator = Paginator(movie_list, per_page)
    movie_list = paginator.page(1)
    context = {
            'movie_list': movie_list,
            'page_title': '近期热搜榜',
            }
    return render(request, 'movie/index.html', context)

@cache_page(60 * 15)
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id  = movie_id)
    resou_movie_list = Movie.objects.order_by('-v_views')[:7]
    # 阅读量自增 1
    movie.increase_views()

    # 是否展示支付宝 领红包 js代码
    alipay_code = "0"
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie': movie,
            'resou_movie_list': resou_movie_list,
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

        if urlstate == 1:
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
        else:
            # 多次点击重置按钮
            info='[CODE:8002] 管理员正在努力重新补链接中...'

    # 已有人报告过该失效链接
    else:
        info='[CODE:8003] 管理员正在努力重新补链接中...'

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

def spiderlog(request):
    # log_list
    log_list = []
    rel =  '/usr/bdpan_movie/daily/pandy/spider/autoSpider_log.txt'
    # rel = '/home/lynn/github_project/daily/pandy/spider/autoSpider_log.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list.append(line)
        f.close()
        '''
        with open (rel, 'r') as f:
            for line in f.readlines():
                log_list.append(line)
        '''
    except:
        log_list.append('The log file doesn^t exsist')

    # log_list_err
    log_list_err = []
    rel =  '/usr/bdpan_movie/daily/pandy/spider/autoSpider_log_error.txt'
    # rel = '/home/lynn/github_project/daily/pandy/spider/autoSpider_log_error.txt'
    try:
        f = codecs.open(rel, 'r', 'utf-8')
        for line in f:
            log_list_err.append(line)
        f.close()
        '''
        with open (rel, 'r') as f:
            for line in f.readlines():
                log_list_err.append(line)
        '''
    except:
        log_list_err.append('The log_err file doesn^t exsist')


    context = {}
    context['log_list'] = log_list
    if len(log_list):
        context['start'] = log_list[0]
        context['end'] = log_list[-1]
    else:
        context['start'] = ''
        context['end'] = ''
    context['log_list_err'] = log_list_err
    return render(request, 'movie/spiderlog.html', context)

def clean_spiderlog(requste):
    msg = ''
    rel = '/usr/bdpan_movie/daily/pandy/spider/autoSpider_log.txt'
    # rel = '/home/lynn/github_project/daily/pandy/spider/autoSpider_log.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '清空 spiderlog 成功'
    except Exception as e:
        msg += '清空 spiderlog 失败'


    rel = '/usr/bdpan_movie/daily/pandy/spider/autoSpider_log_error.txt'
    # rel = '/home/lynn/github_project/daily/pandy/spider/autoSpider_log_error.txt'
    try:
        with open(rel, 'w') as f:
            f.write('')
            msg += '  清空 spiderlog_err 成功'
    except Exception as e:
        msg += '  清空 spiderlog_err 失败'
    return HttpResponse(msg)

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
