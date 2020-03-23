# Create your views here.
from .models import Books
from onlineplay.models import Onlineplay
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.cache import cache_page

# 分页
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
@cache_page(60 * 15)
def book_index(request):
    book_list = Books.objects.all().order_by('-id')
    # 一页的数据数据
    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator( book_list, per_page )

    try:
        # 获取第一页的数据并返回
        book_list = paginator.page(1)
    except:
        # book_list = paginator.page(1)
        book_list = []

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'book_list': book_list,
            'resou_book_list': resou_book_list,
            'page_title': '',
            'url_name': 'book_index', # 传递给模板，用以区别显示 页码 链接
            }
    return render(request, 'books/index.html', context)


@cache_page(60 * 15)
def index_by_page(request, page_num):
    tmp = 1
    try:
        tmp = int(page_num)
    except:
        pass
    page_num = tmp

    # 一页的数据数目
    per_page = 12
    book_list = Books.objects.all().order_by('-id')
    # 生成 paginator 对象
    paginator = Paginator( book_list, per_page )

    try:
        # 获取当前页码中的数据记录
        book_list = paginator.page(page_num)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'book_list': book_list,
            'resou_book_list': resou_book_list,
            'page_title': '',
            'url_name': 'book_index_by_page',
            }

    return render(request, 'books/index.html', context)

# 正常通过 navbar 中的 Form 搜索
def book_search_navbar(request):
    book_name = ''
    try:
        book_name = request.GET['book_name']
    except:
        pass

    # 尝试获取页码
    page_num = 1
    try:
        page_num = request.GET['page_num']
    except:
        # page_num = 1
        pass

    book_list = Books.objects.filter(book_title__icontains=book_name).order_by('-id')

    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator(book_list, per_page)
    # 获取当前页码中的数据记录
    book_list = paginator.page(page_num)

    # 获取图书热搜榜
    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'book_list': book_list,
            'resou_book_list': resou_book_list,
            'book_name': book_name,
            'page_title': book_name+' 搜索结果',
            'url_name': 'book_search_navbar',
            }
    return render(request, 'books/index.html', context)


# 热搜榜，根据访问量返回阅读量最高的20部电影
@cache_page(60 * 15)
def book_resou(request):
    # book_list = book.objects.order_by('-book_views')[:20]
    book_list = Books.objects.order_by('-book_views')[:20]
    # 热搜页 一页的 电影数量
    per_page = 20
    paginator = Paginator(book_list, per_page)
    book_list = paginator.page(1)
    context = {
            'book_list': book_list,
            'page_title': '近期热搜榜',
            }
    return render(request, 'book/index.html', context)


@cache_page(60 * 15)
def book_detail(request, book_id):
    book = get_object_or_404(Books, id  = book_id)
    resou_book_list = Books.objects.order_by('-book_views')[:10]

    # 提取 网盘链接 并构造字典列表 传入 template
    pan_url_list = get_pan_list(book)

    # 阅读量自增 1
    book.increase_views()

    context = {
            'book': book,
            'resou_book_list': resou_book_list,
            'pan_url_1': pan_url_list[0],
            'pan_url_2': pan_url_list[1],
            'pan_url_3': pan_url_list[2],
            }

    return render(request, 'books/detail.html', context)


@cache_page(60 * 15)
def book_category(request):
    # 尝试获取 book_category
    book_category = ''
    try:
        book_category = request.GET['book_category']
    except:
        pass

    # 尝试获取页码
    page_num = 1
    try:
        page_num = request.GET['page_num']
    except:
        # page_num = 1
        pass

    # book_list = Books.objects.filter(book_category__icontains = book_category)
    book_list = Books.objects.filter(book_category = book_category).order_by('-id')

    per_page = 12
    # 生成 paginator 对象
    paginator = Paginator(book_list, per_page)
    # 获取当前页码中的数据记录
    book_list = paginator.page(page_num)

    # 获取图书热搜榜
    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'book_list': book_list,
            'resou_book_list': resou_book_list,
            'book_name': book_category,
            'page_title': book_category +' 免费图书网盘资源下载',
            'url_name': 'book_category',
            'book_category': book_category,
            }
    return render(request, 'books/index.html', context)



# 工具函数
# 解析 book item 的 pan url，并按条件输出
def get_pan_list(book):
    pan_url_list = []
    pan_1 = book.book_pan_1
    pan_2 = book.book_pan_2
    pan_3 = book.book_pan_3

    if len(pan_1):
        pan_url = {}
        pan_url['name'] = pan_1[:4]
        pan_url['url'] = pan_1[6:]
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    if len(pan_2):
        pan_url = {}
        pan_url['name'] = pan_2[:4]
        pan_url['url'] = pan_2[6:]
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    if len(pan_3):
        pan_url = {}
        pan_url['name'] = pan_3[:4]
        pan_url['url'] = pan_3[6:]
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    return pan_url_list

