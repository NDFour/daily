from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Article

from books.models import Books

# 使用 markdown 写文章
import markdown

import sqlite3
import traceback


# Create your views here.

@cache_page(60 * 2)
def index(request):

    # return render(request, 'index/system_pause.html', {})



    article_list = Article.objects.filter( display = True ).order_by('-prior')[:6]
    # article_list = Article.objects.filter( display = True ).order_by('-article_modefy_date')

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'article_list': article_list,
            'resou_book_list': resou_book_list,
            'notifications': article_list,
            }


    # 随机推荐
    random_books = Books.objects.filter(book_valid__gt = 0).order_by('?')[:20]
    context['random_books'] = random_books

    return render(request, 'article/index.html', context)


@cache_page(60 * 2)
def article_detail(request, article_id):

    # return render(request, 'index/system_pause.html', {})
    


    article = get_object_or_404(Article, id  = article_id)
    
    article_list = Article.objects.filter( display = True ).order_by('-prior')[:6]

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    try:
        # 阅读量自增 1
        article.increase_views()

        # 将 markdown 语法渲染成 html 样式
        article.body = markdown.markdown(article.body,
            extensions = [
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            ])
    except Exception as e:
        pass

    context = {
            'article': article,
            'resou_book_list': resou_book_list,
            'notifications': article_list,
            }

    # 随机推荐
    random_books = Books.objects.filter(book_valid__gt = 0).order_by('?')[:20]
    context['random_books'] = random_books


    return render(request, 'article/detail.html', context)






# 根据影片名 搜索影视
def search_magnet(request, movie_name):
    db_name = 'gaoqing_fm_2021_1_8.sqlite3'

    movie_list = []

    msg = ''
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # sql = "select name,url_m3u8 from movies where id=" + str(id)
        sql = "select id, name, pic, content from movies where name" + " like '%" + movie_name + "%' order by length(name) limit 30"
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        if not rel:
            msg = '你好，没有找到名为 ' + str(movie_name) + ' 的影片，请检查你的输入 ~'
        else:
            for m in rel:
                m_item = {
                    'id': m[0],
                    'name': m[1],
                    'pic': m[2],
                    'content': m[3]
                }
                movie_list.append(m_item)

    except Exception as e:
        # print(e)
        # traceback.print_exc()
        msg = '你好，没有找到名为 ' + str(movie_name) + ' 的影片，请检查你的输入 ~'
    finally:
        # print('get_by_id finally 执行了')
        cursor.close()
        conn.close()

    context = {
        'movie_name': movie_name,
        'movie_list': movie_list,
        'len': len(movie_list),
        'msg': msg
    }
    print(msg)

    return render(request, 'article/magnet_list.html', context)



# 根据 电影 ID 获取其 磁力链接 并展示
def magnet_by_id(request, movie_id):
    db_name = 'gaoqing_fm_2021_1_8.sqlite3'

    name = ''
    pic = ''
    content = ''
    magnet_list = []

    msg = ''
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # sql = "select name,url_m3u8 from movies where id=" + str(id)
        sql = "select name, pic, content, magnet from movies where id=" + str(movie_id)
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        if not rel:
            msg = '你好，没有找到 ID 为 ' + str(movie_id) + ' 的影片，请检查你的输入 ~'
        else:
            name = rel[0][0]
            pic = rel[0][1]
            content = rel[0][2]

            chatper_list = rel[0][3].split('##')[:-1]
            # 分割 磁力链接
            for url in chatper_list:
                magnet = {
                    'title': '',
                    'size': '',
                    'definition': '',
                    'url': ''
                }

                if len(url):
                    tag = url.split('#')

                    magnet['title'] = tag[0]
                    magnet['size'] = tag[1]
                    magnet['definition'] = tag[2]
                    magnet['url'] = tag[4]

                    magnet_list.append(magnet)

                    # msg += '<a href="' + tag[4] + '">【' + tag[2] + '】(' + tag[1] + ') ' + tag[0] + '</a>\n\n'
                else:
                    pass
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        msg = '你好，没有找到 ID 为 ' + str(movie_id) + ' 的影片，请检查你的输入 ~'
    finally:
        # print('get_by_id finally 执行了')
        cursor.close()
        conn.close()

    context = {
        'name': name,
        'pic': pic,
        'content': content,
        'magnet_list': magnet_list,
        'msg': msg,
        'has_data': len(msg)
    }

    return render(request, 'article/magnet_detail.html', context)

