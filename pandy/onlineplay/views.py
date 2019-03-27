from .models import Onlineplay
from movie.models import Passwds
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage
import re
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 15)
def onlineplay_index(request):
    movie_list = Onlineplay.objects.filter(v_vip = 0).order_by('-v_pub_date')
    # 一页的数据数据
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取第一页的数据并返回
        movie_list = paginator.page(1)
    except:
        movie_list = paginator.page(1)

    resou_movie_list = Onlineplay.objects.filter( v_vip = 0 ).order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'onlineplay_index', # 传递给模板，用以区别显示 页码 链接
            }
    return render(request, 'movie/index.html', context)


@cache_page(60 * 15)
def onlineplay_index_by_page(request, page_num):
    try:
        tmp = int(page_num)
    except:
        tmp = 1
    page_num = tmp

    movie_list = Onlineplay.objects.filter(v_vip = 0).order_by('-v_pub_date')
    # 一页的数据数目
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( movie_list, per_page )

    try:
        # 获取当前页码中的数据记录
        movie_list = paginator.page(page_num)
    except EmptyPage:
        movie_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页

    resou_movie_list = Onlineplay.objects.filter( v_vip = 0 ).order_by('-v_views')[:7]

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'page_title': '',
            'url_name': 'onlineplay_index_by_page',
            }

    return render(request, 'movie/index.html', context)

# 不能加缓存，不然用户充值之后数据要好长时间更新
def onlineplay_detail(request, movie_id):
    movie = get_object_or_404(Onlineplay, id  = movie_id)

    # 分割视频播放 url
    playurls = []
    sourceurls = movie.v_playurl.split('$$')
    for s in sourceurls:
        urls_tmp = s.split('$')
        # 免费解析接口
        urls_tmp2 = []
        for url_tmp in urls_tmp:
            if re.match(r'.*www.mgtv.com.*',url_tmp):
                urls_tmp2.append('https://jiexi.gysc88.cn//mdparse/index.php?id=' + url_tmp)
            elif re.match(r'.*v.qq.com.*',url_tmp):
                urls_tmp2.append('https://api.flvsp.com/?url=' + url_tmp)
            elif re.match(r'.*letv.com.*',url_tmp):
                urls_tmp2.append('https://jiexi.gysc88.cn//mdparse/index.php?id=' + url_tmp)
            elif re.match(r'.*iqiyi.com.*',url_tmp):
                urls_tmp2.append('https://www.1616v.com/1616/?url=' + url_tmp)
            else:
                urls_tmp2.append(url_tmp)
        playurls.append(urls_tmp2)
    playurls[-1].pop()

    # 跳转到 detail 页先播放第一集
    try:
        index_video = playurls[0][1]
    except:
        index_video = ''

    resou_movie_list = Onlineplay.objects.filter( v_vip = 0 ).order_by('-v_views')[:7]
    # 阅读量自增 1
    movie.increase_views()

    # 是否展示支付宝 领红包 js代码
    alipay_code = "0"
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    # 判断用户是否登录以及是否为 vip 用户
    is_vip = request.session.get('user_isvip', default=None)

    context = {
            'movie': movie,
            'is_vip': is_vip,
            'playurls': playurls,
            'index_video': index_video,
            'resou_movie_list': resou_movie_list,
            'alipay_code': alipay_code,
            }

    return render(request, 'onlineplay/detail.html', context)


def getVipByCode(request, vipCode):
    """ 根据 v_vip 的字段获取同字段所有条目
    """

    movie_list = Onlineplay.objects.filter( v_vip = vipCode )

    # 获取在线热搜榜
    resou_movie_list = Onlineplay.objects.filter( v_vip = 0 ).order_by('-v_views')[:7]

    # 是否展示支付宝 领红包 js代码
    alipay_code = '0'
    alipay_obj = get_object_or_404(Passwds, p_code=1002)
    if alipay_obj:
        alipay_code = alipay_obj.p_value

    context = {
            'movie_list': movie_list,
            'resou_movie_list': resou_movie_list,
            'movie_name': str( vipCode ),
            'page_title': str( vipCode ) + ' 搜索结果',
            'alipay_code': alipay_code,
            'url_name': 'getVipByCode',
            }
    return render(request, 'movie/index.html', context)
    # return HttpResponse('search page %s' % movie_name)
