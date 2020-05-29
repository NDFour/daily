# Create your views here.
from .models import Books
from .models import Babaili_jiaji
'''
from .models import Book_notify
'''
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.views.decorators.cache import cache_page

# 分页
from django.core.paginator import Paginator, EmptyPage

import time
import csv

# 搜索结果 按 名字长度 排序
from django.db.models.functions import Length

# Create your views here.
@cache_page(60 * 15)
def book_index(request):
    book_list = Books.objects.all().order_by('-id')
    # 一页的数据数据
    per_page = 24
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
    per_page = 24
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
    # 尝试获取 来源页 URL
    origin_full_url = ''
    try:
        # 带参数 URL
        origin_full_url = request.get_full_path()
    except Exception as e:
        pass

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

    # book_list = Books.objects.filter(book_title__icontains=book_name).order_by('-id')
    book_list = Books.objects.filter(book_title__icontains=book_name).order_by(Length("book_title").asc())

    per_page = 24
    # 生成 paginator 对象
    paginator = Paginator(book_list, per_page)
    # 获取当前页码中的数据记录
    try:
        book_list = paginator.page(page_num)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页




    # 获取图书热搜榜
    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'book_list': book_list,
            'resou_book_list': resou_book_list,
            'book_name': book_name,
            'page_title': book_name+' 搜索结果',
            'url_name': 'book_search_navbar',
            'origin_full_url': origin_full_url,
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
    # 尝试获取 来源页 URL
    origin_full_url = ''
    try:
        # 带参数 URL
        origin_full_url = request.get_full_path()
    except Exception as e:
        pass

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
            'url_name': 'book_detail',
            'origin_full_url': origin_full_url,
            }

    return render(request, 'books/detail.html', context)


# 获取某一分类的所有图书 分页展示
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

    per_page = 24
    # 生成 paginator 对象
    paginator = Paginator(book_list, per_page)
    # 获取当前页码中的数据记录
    try:
        book_list = paginator.page(page_num)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在生成的范围内，显示最后一页




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


# 八百里加急催 信息提交 页面
def invalid_url_report(request):
    # print(book_id)
    # 尝试获取 book_id 以生成 origin_url
    '''
    book_id = 0
    try:
        book_id = request.GET['book_id']
        print('找到 book_id' + str(book_id))
    except:
        print('没有找到 book_id')
        book_id = -1
    '''

    context = {
        # 'book_id': book_id,
        'url_name': 'invalid_url_report',
    }
    return render(request, 'books/invalid_url_report.html', context)


# 八百里加急立即催
# <!-- 图书未搜索到  表单提交 -->
# <!-- 或 -->
# <!-- 图书网盘链接失效  表单提交 -->
def babaili_jiaji(request):

    # msg = '已收到您的八百里加急，除特殊情况外，管理员最迟 48h 内给您消息。\n\n注：管理员有自己的正常生活，非全职，如回复过慢请谅解。谢谢您的理解'
    msg = ''

    # 尝试获取 book_name
    book_name = ''
    try:
        book_name = request.GET['book_name']
    except:
        msg = '没有收到您提交的消息哦'

    # 尝试获取 author, contact_method, other_info, origin_full_url
    author = ''
    contact_method = ''   
    other_info = ''
    origin_full_url = ''
    try:
        author = request.GET['author']
        contact_method = request.GET['contact_method']
        other_info = request.GET['other_info']
        origin_full_url = request.GET['origin_full_url']
    except:
        pass

    # 尝试获取 babaili_jiaji_type
    babaili_jiaji_type = ''
    try:
        babaili_jiaji_type = request.GET['babaili_jiaji_type']
    except:
        msg += ' - 获取 babaili_jiaji_type 失败！'

    # 判断 八百里加急 的 type
    # 写入 babaili_jiaji.csv
    # 如果 msg 内容不为空，说明前面已有错误发生，无需写入 csv
    if not msg:
        # 将信息写入文件 or 数据库
        '''
        csv_status = babali_jiaji_toCsv( book_name, author, contact_method, other_info, babaili_jiaji_type, origin_full_url )
        # -1: failed     0: success
        if csv_status:
            msg += ' - 写入 csv 失败！ 可联系管理员确认原因，微信:ndfour001  邮箱:ndfour@foxmail.com'
        '''
        try:
            new_babaili_item = Babaili_jiaji()
            new_babaili_item.book_name = book_name
            new_babaili_item.author = author
            new_babaili_item.contact_method = contact_method
            new_babaili_item.other_info = other_info
            new_babaili_item.babaili_jiaji_type = babaili_jiaji_type
            new_babaili_item.origin_full_url = origin_full_url
            new_babaili_item.is_solved = False
            new_babaili_item.report_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() )
            new_babaili_item.save()
        except Exception as e:
            msg += ' - 写入记录失败！ 可联系管理员确认原因，微信:ndfour001  邮箱:ndfour@foxmail.com'
            pass

    context = {
        'book_name': book_name,
        'author': author,
        'contact_method': contact_method,
        'other_info': other_info,
        'msg': msg,
    }

    return render(request, 'books/babaili_jiaji_success.html', context)



# 工具函数
# 解析 book item 的 pan url，并按条件输出
def get_pan_list(book):
    pan_url_list = []
    pan_1 = book.book_pan_1
    pan_2 = book.book_pan_2
    pan_3 = book.book_pan_3

    if len(pan_1):
        pan_url = {}
        try:
            tmp1 = pan_1.split('##')
            pan_url['name'] = tmp1[0] + ' 下载'
            pan_url['url'] = tmp1[1]
        except Exception as e:
            pan_url['name'] = '暂无'
            pan_url['url'] = '#'           
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    if len(pan_2):
        pan_url = {}
        try:
            tmp2 = pan_2.split('##')
            pan_url['name'] = tmp2[0] + ' 下载'
            pan_url['url'] = tmp2[1]
        except Exception as e:
            pan_url['name'] = '暂无'
            pan_url['url'] = '#'
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    if len(pan_3):
        pan_url = {}
        try:
            tmp3 = pan_3.split('##')
            pan_url['name'] = tmp3[0] + ' 下载'
            pan_url['url'] = tmp3[1]
        except Exception as e:
            pan_url['name'] = '暂无'
            pan_url['url'] = '#'           
        pan_url_list.append(pan_url)
    else:
        pan_url = {}
        pan_url['name'] = '暂无'
        pan_url['url'] = '#'
        pan_url_list.append(pan_url)

    return pan_url_list


# 工具函数
# 写入数据到 babaili_jiaji.csv 文件
def babali_jiaji_toCsv( book_name, author, contact_method, other_info, babaili_jiaji_type, origin_full_url ):
    try:
        jiaji_item = {
            'book_name': book_name,
            'author': author,
            'contact_method': contact_method,
            'other_info': other_info,
            'babaili_jiaji_type': babaili_jiaji_type,
            'origin_full_url': origin_full_url,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }
        # 写入 csv 文件 ; encoding 解决用 wps 打开后中文乱码
        out_file_name = 'babaili_jiaji.csv'
        # print("OUT:" + out_file_name)
        with open(out_file_name, 'a', encoding = 'utf-8-sig') as csvfile:
            fieldnames = ['book_name', 'author', 'contact_method', 'other_info', 'babaili_jiaji_type', 'time', 'origin_full_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #注意header是个好东西
            # writer.writeheader()
            # for u_items in self.book_item_list:
            #     writer.writerow(u_items)
            writer.writerow( jiaji_item )
        return 0
    except Exception as e:
        return -1

