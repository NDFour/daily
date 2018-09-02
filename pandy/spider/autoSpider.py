# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-09-02 13:57:43
# Last Modified: 2018-09-02 19:29:48
#

import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import pymysql
import time
import os
import traceback

# 记录程序输入，并写入到本地文件，供 web 端展示
str_2_logfile = []
# 记录程序输出行数
line_cnt = 0

class yeyoufang_Spider:
    # 采集网站的目录url
    category_urls = [
            'http://www.yeyoufang.com/fl/dy/page/',
            ]
    # 每次需要更新的页数+1
    pages_num = 5

    def __init__(self):
        global str_2_logfile
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        str_2_logfile.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print('\tmovieSpider for yeyoufang.com')
        str_2_logfile.append('\tmovieSpider for yeyoufang.com')
        # print()
        # print('>> movieSpider init...')
        str_2_logfile.append('\n>> movieSpider init...')
        # 关闭 django 应用 pandy
        # print('>> stop [pandy]')
        # print('\n\n')
        str_2_logfile.append('\n\n')

    # 遍历目录获取电影名保存到列表，删除已存在数据库的，然后获取电影信息
    # 返回值： 1-电影名列表 2-电影详情页url列表 （返回的均为数据库中不存在的)
    def get_url(self):
        global str_2_logfile
        # print('>> [get_url]')
        current_page = 1
        movies_num = 0
        # 以下两个列表用于返回
        title_list = []
        url_list = []

        for category in self.category_urls:
            # 遍历 pages_num 页
            while current_page < self.pages_num:
                # print('>> [get_url] now is page %s\n>> %s\n' % (current_page, category + str(current_page) ) )
                # 构造响应页码目录url，并获取目录页网页 文本
                category_html = self.get_html(category + str(current_page))
                # 只解析 <h2> 标签，其中包含电影名和详情页url
                only_title_href = SoupStrainer("h2")
                soup = BeautifulSoup(category_html, 'lxml', parse_only=only_title_href)
                a_list = soup.find_all('a')
                movies_num += len(a_list)

                for i in a_list:
                    href = i['href']
                    title = i.string
                    # 判断是否已经存在于数据库，是的话跳过，不是则存储
                    if is_saved(href) == 1:
                        # print('>> [get_url] skip already exsist\n  %s' % title)
                        str_2_logfile.append('>> [get_url] skip already exsist\n  %s' % title + '   [yeyoufang]')
                        #print('>> [get_url] already exsist')
                    else:
                        title_list.append(title)
                        url_list.append(href)

                # 页码数 ++ ，构造下一页的目录页url
                current_page += 1

        # print('>> [get_url] total %s movies' % movies_num)
        str_2_logfile.append('>> [get_url] total %s movies' % movies_num)
        return title_list,url_list

    # 解析详情页获得电影信息，返回电影信息 列表
    def get_info(self, detail_url):
        global str_2_logfile
        # print('>> [get_info] %s' % detail_url)
        str_2_logfile.append('>> [get_info] %s' % detail_url)
        detail_html = self.get_html(detail_url)
        # 只解析 <article> 标签，为电影信息模块
        only_article_tag = SoupStrainer("article")
        soup = BeautifulSoup(detail_html, 'lxml', parse_only=only_article_tag)

        try: # 电影名
            movie_name = soup.h1.string
        except:
            movie_name = ''

        try: # 封面图
            movie_pic = soup.img['src']
        except:
            movie_pic = ''

        try: # 简介
            movie_text = ''
            # 查找到所有包含 strong 的标签
            p_list = soup.find_all('p')
            for p in p_list:
                if p.strong:
                    movie_text = p.contents[-1]
            movie_text = movie_text.replace(' ','')
        except:
            movie_text = ''

        try: # 网盘链接
            movie_bdpan = ''
            re_bdpan = re.compile(r'http.*pan.*?"')
            movie_bdpan = re_bdpan.findall(soup.prettify() )[0].replace('"','')
        except:
            movie_bdpan = ''

        try: # 网盘密码
            movie_pass = ''
            re_pass = re.compile(r'密码.*')
            movie_pass = re_pass.findall(soup.prettify())[0]
        except:
            movie_pass = ''

        movie_info_list = []
        movie_info_list.append(movie_name)
        movie_info_list.append(movie_pic)
        movie_info_list.append(movie_text)
        movie_info_list.append(movie_bdpan)
        movie_info_list.append(movie_pass)
        movie_info_list.append(detail_url)

        # 传入影片信息列表保存电影信息
        self.save_2_db(movie_info_list)

    # 接收传入的电影信息作为参数 构造并执行sql 保存数据至db，保存新数据的同时删除旧数据
    # 接收参数： sql_param : 影片的信息
    def save_2_db(self, sql_param):
        global str_2_logfile
        # sql_param: name, pic, text_info, bdpan, pass, href
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_insert = 'INSERT INTO movie_movie(v_name, v_pic, v_text_info, v_bdpan, v_pass, v_href, v_pub_date, v_ed2k, v_magnet, v_ed2k_name, v_magnet_name, v_valid, v_views) VALUES ("%s", "%s", "%s", "%s", "%s",  "%s", "%s", "%s", "%s", "%s", "%s", 1, 0);' % \
        (sql_param[0], sql_param[1], sql_param[2], sql_param[3], sql_param[4], sql_param[5], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '', '', '', '')

        try:
            cursor.execute(sql_insert)
            conn.commit()
            # print('>> [save_2_db] insert succes')
            str_2_logfile.append('>> [save_2_db] insert succes')

            # 检测数据库中是否有和该电影采集页url一致 但是 电影名 不一样（旧版）的，有的话删除
            movie_name = sql_param[0]
            movie_href = sql_param[5]
            sql_del = 'DELETE FROM movie_movie WHERE v_href="%s" AND v_name!="%s";' % (movie_href, movie_name)
            try:
                cursor.execute(sql_del)
                conn.commit()
                # print('>> [save_2_db] del old version success\n')
            except:
                conn.rollback()
                # print('>> [save_2_db] del old version failed\n')
                str_2_logfile.append('>> [save_2_db] del old version failed\n')
        except:
            conn.rollback()
            # print('>> [save_2_db] insert failed')
            str_2_logfile.append('>> [save_2_db] insert failed')

        cursor.close()
        conn.close()

    # 获取网页文本
    def get_html(self,url):
        try:
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
            }
            r = requests.get(url, headers = headers, timeout = 10)
            r.encoding = r.apparent_encoding
            html_text = r.text
        except:
            html_text = ''
        return html_text

class menggouwp_Spider:
    # 采集网站的目录url
    category_urls = [
            'http://www.menggouwp.com/a/dianying/list_1_', # 电影
            'http://www.menggouwp.com/a/dianshiju/list_4_' # 电视剧
            ]
    # 每次需要更新的页数+1
    pages_num = 5

    def __init__(self):
        global str_2_logfile
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        str_2_logfile.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print('\tmovieSpider for yeyoufang.com')
        str_2_logfile.append('\tmovieSpider for menggouwp.com')
        # print()
        # print('>> movieSpider init...')
        str_2_logfile.append('\n>> movieSpider init...')

        # 关闭 django 应用 pandy
        # print('>> stop [pandy]')
        # print('\n\n')
        str_2_logfile.append('\n\n')

    # 遍历目录获取电影名保存到列表，删除已存在数据库的，然后获取电影信息
    # 返回值： 1-电影名列表 2-电影详情页url列表 （返回的均为数据库中不存在的)
    def get_url(self):
        global str_2_logfile
        current_page = 1
        movies_num = 0
        # 以下两个列表用于返回
        title_list = []
        url_list = []

        for category in self.category_urls:
            # 遍历 pages_num 页
            while current_page < self.pages_num:
                # print('>> [get_url] now is page %s\n>> %s\n' % (current_page, category + str(current_page) + '.html' ) )
                # 构造响应页码目录url，并获取目录页网页 文本
                category_html = self.get_html(category + str(current_page) + '.html' )
                # 只解析 <h2> 标签，其中包含电影名和详情页url
                only_title_href = SoupStrainer(class_='d-block')
                soup = BeautifulSoup(category_html, 'lxml', parse_only=only_title_href)
                a_list = soup.find_all('a')
                small_list = soup.find_all(class_='d-block p-1 text-dark')
                movies_num += len(a_list)

                url_cnt = 0
                for i in a_list:
                    href = 'http://www.menggouwp.com' + i['data-href']
                    title = small_list[url_cnt].string
                    # 判断是否已经存在于数据库，是的话跳过，不是则存储
                    # str_2_logfile.append('http://www.menggouwp.com' + href)
                    if is_saved( href) == 1:
                        # print('>> [get_url] skip already exsist\n  %s' % title)
                        str_2_logfile.append('>> [get_url] skip already exsist\n  %s' % title + '   [menggouwp]')
                        # print('>> [get_url] already exsist')
                        url_cnt += 1
                    else:
                        url_list.append(href)
                        title_list.append(title)
                        url_cnt += 1

                # 页码数 ++ ，构造下一页的目录页url
                current_page += 1

        # print('>> [get_url] total %s movies' % movies_num)
        str_2_logfile.append('>> [get_url] total %s movies' % movies_num)
        return title_list,url_list

    # 解析详情页获得电影信息，返回电影信息 列表
    def get_info(self, detail_url):
        global str_2_logfile
        # print('>> [get_info] %s' % detail_url)
        str_2_logfile.append('>> [get_info] %s' % detail_url)

        detail_html = self.get_html(detail_url)
        # 只解析 <main> 标签，为电影信息模块
        only_article_tag = SoupStrainer("main")
        soup = BeautifulSoup(detail_html, 'lxml', parse_only=only_article_tag)

        try: # 电影名
            movie_name = soup.h3.string
        except:
            movie_name = ''

        try: # 封面图
            movie_pic = soup.find('img')['data-original']
        except:
            movie_pic = ''

        movie_text = '暂无影片简介'

        try: # 网盘链接
            movie_bdpan = ''
            movie_bdpan = soup.find(class_='mr-auto text-info')['href']
        except:
            movie_bdpan = ''

        try: # 网盘密码
            movie_pass = ''
            movie_pass = soup.find(class_='mr-2').get_text()
        except:
            movie_pass = ''

        movie_info_list = []
        movie_info_list.append(movie_name)
        movie_info_list.append(movie_pic)
        movie_info_list.append(movie_text)
        movie_info_list.append(movie_bdpan)
        movie_info_list.append(movie_pass)
        movie_info_list.append(detail_url)

        # 传入影片信息列表保存电影信息
        self.save_2_db(movie_info_list)

    # 接收传入的电影信息作为参数 构造并执行sql 保存数据至db，保存新数据的同时删除旧数据
    # 接收参数： sql_param : 影片的信息
    def save_2_db(self, sql_param):
        global str_2_logfile
        # sql_param: name, pic, text_info, bdpan, pass, href
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_insert = 'INSERT INTO movie_movie(v_name, v_pic, v_text_info, v_bdpan, v_pass, v_href, v_pub_date, v_ed2k, v_magnet, v_ed2k_name, v_magnet_name, v_valid, v_views) VALUES ("%s", "%s", "%s", "%s", "%s",  "%s", "%s", "%s", "%s", "%s", "%s", 1, 0);' % \
        (sql_param[0], sql_param[1], sql_param[2], sql_param[3], sql_param[4], sql_param[5], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '', '', '', '')

        try:
            cursor.execute(sql_insert)
            conn.commit()
            # print('>> [save_2_db] insert succes')
            str_2_logfile.append('>> [save_2_db] insert succes')

            # 检测数据库中是否有和该电影采集页url一致 但是 电影名 不一样（旧版）的，有的话删除
            movie_name = sql_param[0]
            movie_href = sql_param[5]
            sql_del = 'DELETE FROM movie_movie WHERE v_href="%s" AND v_name!="%s";' % (movie_href, movie_name)
            try:
                cursor.execute(sql_del)
                conn.commit()
                # print('>> [save_2_db] del old version success\n')
            except:
                conn.rollback()
                # print('>> [save_2_db] del old version failed\n')
                str_2_logfile.append('>> [save_2_db] del old version failed\n')
        except:
            conn.rollback()
            # print('>> [save_2_db] insert failed')
            str_2_logfile.append('>> [save_2_db] insert failed')

        cursor.close()
        conn.close()

    # 获取网页文本
    def get_html(self,url):
        global str_2_logfile
        try:
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.menggouwp.com',
            'If-Modified-Since': 'Thu, 30 Aug 2018 12:55:35 GMT',
            'If-None-Match': 'W/"5b87e947-303e"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            r = requests.get(url, timeout = 10)
            r.encoding = r.apparent_encoding
            html_text = r.text
            # print('>> [get_html] success %s' %len(html_text))
            str_2_logfile.append('>> [get_html] success' )
        except:
            html_text = ''
            # print('>> [get_html] failed')
            str_2_logfile.append('>> [get_html] failed : %s' %url)
        return html_text

# 判断传入的 影片名 是否已存在于数据库
def is_saved( href):
    global str_2_logfile
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='bdpan',charset='utf8')
    cursor=conn.cursor()

    sql_select = "SELECT * FROM movie_movie WHERE v_href='%s';" % href
    target_num = 0
    try:
        target_num = cursor.execute(sql_select)
    except:
        pass
    cursor.close()
    conn.close()

    if target_num == 0:
        return 0
    return 1

def write_2_logfile(log_list):
    global line_cnt
    try:
        with open('/usr/bdpan_movie/daily/pandy/spider/autoSpider_log.txt', 'a') as f:
            for log in log_list:
                f.write(str(line_cnt) + ' ' + log + '\n')
                line_cnt += 1
    except:
        with open('/usr/bdpan_movie/daily/pandy/spider/autoSpider_log_error.txt', 'a') as er:
            er.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) )
            er.write('[write_2_logfile] write_2_logfile failed')
            er.write('\n\n\n')

# 删除数据库中 v_href 重复的数据项，只保留 id 最大的一项
def del_copy_movies():
    global str_2_logfile
    conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
    cursor = conn.cursor()

    sql_del_copy = "DELETE FROM movie_movie WHERE v_href IN (SELECT v_href FROM movie_movie GROUP BY v_href HAVING count(v_href) > 1 ) AND id NOT IN ( SELECT max(id) FROM movie_movie GROUP BY v_href HAVING count(v_href) > 1 );"
    try:
        cursor.execute(sql_del_copy)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    str_2_logfile.append('\n删除数据库中重复数据成功\n')

def main():
    global str_2_logfile

    str_2_logfile.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    str_2_logfile.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print('\t autoSpider\n\t\tthe god of the spider')
    str_2_logfile.append('\t autoSpider\n\t\tthe god of the spider')
    # print()
    str_2_logfile.append('\n')
    # pritn('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    str_2_logfile.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    # print()

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    yeyoufang = yeyoufang_Spider()
    title_list, url_list = yeyoufang.get_url()
    str_2_logfile.append('---------- yeyoufang 共有 %s 条数据需要插入 --------' % len(url_list))
    for detail_url in url_list:
        yeyoufang.get_info(detail_url)

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    menggouwp = menggouwp_Spider()
    title_list, url_list = menggouwp.get_url()
    str_2_logfile.append('---------- menggouwp 共有 %s 条数据需要插入 --------' % len(url_list))
    for detail_url in url_list:
        menggouwp.get_info(detail_url)

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    # print()
    # print('--------------------------------')
    str_2_logfile.append('\n--------------------------------')
    # print('autoSpider done !')
    str_2_logfile.append('autoSpider done !')
    str_2_logfile.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 删除数据库中 v_href 重复的数据
    # del_copy_movies()

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

main()
