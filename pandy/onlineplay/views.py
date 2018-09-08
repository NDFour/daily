from .models import Onlineplay
from movie.models import Passwds
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage

# Create your views here.
def onlineplay_index(request):
    movie_list = Onlineplay.objects.all().order_by('-v_pub_date')
    # 一页的数据数据
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取第一页的数据并返回
        movie_list = paginator.page(1)
    except:
        movie_list = paginator.page(1)

    resou_movie_list = Onlineplay.objects.order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'onlineplay_index', # 传递给模板，用以区别显示 页码 链接
            }
    return render(request, 'movie/index.html', context)

def onlineplay_index_by_page(request, page_num):
    try:
        tmp = int(page_num)
    except:
        tmp = 1
    page_num = tmp

    movie_list = Onlineplay.objects.all().order_by('-v_pub_date')
    # 一页的数据数目
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取当前页码中的数据记录
        movie_list = paginator.page(page_num)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页

    resou_movie_list = Onlineplay.objects.order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'onlineplay_index_by_page',
            }

    return render(request, 'movie/index.html', context)

def onlineplay_detail(request, movie_id):
    movie = get_object_or_404(Onlineplay, id  = movie_id)

    # 分割视频播放 url
    playurls = []
    sourceurls = movie.v_playurl.split('$$')
    for s in sourceurls:
        urls_tmp = s.split('$')
        playurls.append(urls_tmp)
    playurls[-1].pop()

    # 跳转到 detail 页先播放第一集
    try:
        index_video = playurls[0][1]
    except:
        index_video = ''

    resou_movie_list = Onlineplay.objects.order_by('-v_views')[:7]
    # 阅读量自增 1
    movie.increase_views()

    # 是否展示支付宝 领红包 js代码
    alipay_code = "0"
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie': movie,
            'playurls': playurls,
            'index_video': index_video,
            'resou_movie_list': resou_movie_list,
            'alipay_code': alipay_code,
            }

    return render(request, 'onlineplay/detail.html', context)
