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
import sys
import traceback
import codecs
import json

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
                    if is_saved(href, 1) == 1:
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
                    if is_saved( href, 1) == 1:
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

class kuyunzy_Spider:
    # 采集网站的目录url
    category_urls = [
            'http://www.kuyunzy.cc/list/?0-', # 电影
            ]
    # 每次需要更新的页数+1
    pages_num = 5

    def __init__(self):
        global str_2_logfile
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        str_2_logfile.append('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print('\tmovieSpider for yeyoufang.com')
        str_2_logfile.append('\tmovieSpider for kuyunzy.cc')
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
            current_page = 1
            # 遍历 pages_num 页
            while current_page < self.pages_num:
                # print('>> [get_url] now is page %s\n>> %s\n' % (current_page, category + str(current_page) + '.html' ) )
                # 构造响应页码目录url，并获取目录页网页 文本
                category_html = self.get_html(category + str(current_page) + '.html' )
                # 只解析 align="left"的<td> 标签，其中包含电影名和详情页url
                # <td height="20" align="left"><a href="/detail/?15422.html" target="_blank">小生梦惊魂&nbsp;</a></td>
                only_title_href = SoupStrainer(align="left")
                soup = BeautifulSoup(category_html, 'lxml', parse_only=only_title_href)
                a_list = soup.find_all('a')
                movies_num += len(a_list)

                for i in a_list:
                    href = 'http://www.kuyunzy.cc' + i['href']
                    title = i.string
                    # 判断是否已经存在于数据库，是的话跳过，不是则存储
                    # str_2_logfile.append('http://www.menggouwp.com' + href)
                    if is_saved( href, 2) == 1:
                        # print('>> [get_url] skip already exsist\n  %s' % title)
                        str_2_logfile.append('>> [get_url] skip already exsist\n  %s' % title + '   [kuyunzy]')
                        # print('>> [get_url] already exsist')
                    else:
                        url_list.append(href)
                        title_list.append(title)

                # 页码数 ++ ，构造下一页的目录页url
                current_page += 1

        # print('>> [get_url] total %s movies' % movies_num)
        str_2_logfile.append('>> [get_url] total %s movies' % movies_num)
        return title_list,url_list

    # 解析详情页获得电影信息，返回电影信息 列表
    def get_info(self, detail_url, movie_name):
        global str_2_logfile
        # print('>> [get_info] %s' % detail_url)
        str_2_logfile.append('>> [get_info] %s' % detail_url)

        detail_html = self.get_html(detail_url)
        soup = BeautifulSoup(detail_html, 'lxml')

        try: # 封面图
            movie_pic = soup.find_all('img')[1]['src']
        except:
            movie_pic = ''

        try: # 影片简介
            movie_text = ''
            re_text = re.compile(r"介绍开始代码-->.*<!--")
            movie_text = re_text.findall(detail_html)[0].replace('介绍开始代码-->','').replace('<!--','').replace('"','').replace("'",'').replace("\\",'')
        except:
            movie_text = '影片介绍暂时为空'

        try: # 在线播放链接
            movie_playurl = ''
            # 只解析视频链接部分 html 代码
            only_span_2 = SoupStrainer(colspan="2")
            soup = BeautifulSoup(detail_html, 'lxml', parse_only=only_span_2)

            titles_set = soup.find_all('h1')
            titles = []
            for t in titles_set:
                titles.append(t.string)
            # 最终 movie_playurl 形式： 来源1$ url1 $ url2 $ url3 $$ 来源2 $ url1 $ url2....
            ziyuan_cnt = 0
            for ziyuan in soup.find_all('table'):
                v_title = titles[ziyuan_cnt]
                ziyuan_cnt += 1
                movie_playurl += v_title
                movie_playurl += '$'
                v_urls = ziyuan.find_all(id="copy_yah")
                for url in v_urls:
                    movie_playurl += url['value']
                    movie_playurl += '$'
                movie_playurl += '$'
        except:
            movie_playurl = ''

        movie_info_list = []
        movie_info_list.append(movie_name)
        movie_info_list.append(movie_pic)
        movie_info_list.append(movie_text)
        movie_info_list.append(movie_playurl)
        movie_info_list.append(detail_url)

        ''' print 采集到的播放链接
        for i in movie_playurl.split('$$'):
            print('第一个来源')
            print('总共有 %s 个来源' % len(movie_playurl.split('$$') ) )
            print('该来源共有 %s 个资源' % len(i.split('$')))
            print()
            for j in i.split('$'):
                print(j)
        '''

        # 传入影片信息列表保存电影信息
        self.save_2_db(movie_info_list)

    # 接收传入的电影信息作为参数 构造并执行sql 保存数据至db，保存新数据的同时删除旧数据
    # 接收参数： sql_param : 影片的信息
    def save_2_db(self, sql_param):
        global str_2_logfile
        # sql_param: name, pic, text_info, playurl, href
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_insert = 'INSERT INTO onlineplay_onlineplay(v_name, v_pic, v_text_info, v_playurl, v_href, v_pub_date, v_views) VALUES ("%s", "%s", "%s", "%s", "%s",  "%s", 0);' % \
        (sql_param[0], sql_param[1], sql_param[2], sql_param[3], sql_param[4], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) )

        try:
            cursor.execute(sql_insert)
            conn.commit()
            # print('>> [save_2_db] insert succes')
            str_2_logfile.append('>> [save_2_db] insert succes')

            # 检测数据库中是否有和该电影采集页url一致 但是 电影名 不一样（旧版）的，有的话删除
            movie_name = sql_param[0]
            movie_href = sql_param[4]
            sql_del = 'DELETE FROM onlineplay_onlineplay WHERE v_href="%s" AND v_name!="%s";' % (movie_href, movie_name)
            try:
                cursor.execute(sql_del)
                conn.commit()
                # print('>> [save_2_db] del old version success\n')
            except:
                conn.rollback()
                # print('>> [save_2_db] del old version failed\n')
                str_2_logfile.append('>> [save_2_db] del old version failed\n')
        except:
            str_2_logfile.append(sys.exc_info())
            conn.rollback()
            # print('>> [save_2_db] insert failed')
            str_2_logfile.append('>> [save_2_db] insert failed')
            str_2_logfile.append(sql_insert)

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
            'Host': 'www.kuyunzy.cc',
            'Referer': 'http://www.kuyunzy.cc/list/?0.html',
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

class xujiating_Spider:
    # 0-*, 12-*
    # 1,5,6,7,8,9,10,11,18,19 罗拉电影
    # typeid:
    # 电影： 5-动作片 6-喜剧 8-科幻 9-恐怖 10-剧情 11-战争 18-惊悚 (2,7, 16-爱奇艺直链 1-不好用)
    # 电视剧： 12-国产剧 13-港台剧 14-日韩剧 15-欧美剧
    # 动漫： 4-动漫
    # 综艺 3-综艺
    url = 'http://w.xujiating.cn/index.php/home/index/addpian.html'
    pages_num = 772
    current_page = 0

    def get_info(self):
        global str_2_logfile
        data = {
            'start': '0',
            'typeid': '1,5,6,7,8,9,10,11,18,19',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '57',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'w.xujiating.cn',
            'Origin': 'http://w.xujiating.cn',
            'Referer': 'http://w.xujiating.cn/index.php/home/index/dianying.html',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'X-Requested-With': 'XMLHttpRequest'
        }

        while self.current_page < self.pages_num:
            data['start'] = str(self.current_page*12)
            try:
                r = requests.post(self.url, data=data, headers = headers)
                parsed_json = json.loads(r.text[307:])
            except:
                empt_dic = '{"info":"0"}'
                parsed_json = json.loads(empt_dic)
                # str_2_logfile.append(sys.exc_info() )
                str_2_logfile.append('>> [get_info] 获取 json 数据失败 start: %s' %data['start'])

            if parsed_json['info'] == 1:
                if parsed_json['conter']:
                    for movie in parsed_json['conter']:
                        if is_saved(movie['d_id'], 2):
                            str_2_logfile.append('>> [get_info] skip already exsist\n %s' % movie['d_name'] + '   [xujiating]')
                        else:
                            movie_info_list = []
                            movie_info_list.append(movie['d_name'])
                            movie_info_list.append(movie['d_pic'])
                            movie_info_list.append(movie['d_content'].replace('"','').replace("'",''))
                            movie_info_list.append(movie['d_playurl'].replace('#','$$').replace('$$$','$$')+'$$')
                            movie_info_list.append(movie['d_id']) # detail_url
                            self.save_2_db(movie_info_list)

            write_2_logfile(str_2_logfile)
            str_2_logfile = []
            self.current_page += 1

    def save_2_db(self, sql_param):
        global str_2_logfile
        # sql_param: name, pic, text_info, playurl, href
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_insert = 'INSERT INTO onlineplay_onlineplay(v_name, v_pic, v_text_info, v_playurl, v_href, v_pub_date, v_views) VALUES ("%s", "%s", "%s", "%s", "%s",  "%s", 0);' % \
        (sql_param[0], sql_param[1], sql_param[2], sql_param[3], sql_param[4], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) )

        try:
            cursor.execute(sql_insert)
            conn.commit()
            # print('>> [save_2_db] insert succes')
            str_2_logfile.append('>> [save_2_db] insert succes')

            # 检测数据库中是否有和该电影采集页url一致 但是 电影名 不一样（旧版）的，有的话删除
            movie_name = sql_param[0]
            movie_href = sql_param[4]
            sql_del = 'DELETE FROM onlineplay_onlineplay WHERE v_href="%s" AND v_name!="%s";' % (movie_href, movie_name)
            try:
                cursor.execute(sql_del)
                conn.commit()
                # print('>> [save_2_db] del old version success\n')
            except:
                conn.rollback()
                # print('>> [save_2_db] del old version failed\n')
                str_2_logfile.append('>> [save_2_db] del old version failed\n')
        except:
            str_2_logfile.append(sys.exc_info())
            conn.rollback()
            # print('>> [save_2_db] insert failed')
            str_2_logfile.append('>> [save_2_db] insert failed')
            str_2_logfile.append(sql_insert)

        cursor.close()
        conn.close()

# 判断传入的 影片名 是否已存在于数据库
# table = 1 时，查 movie_movie 表，对应网盘
# table = 2 时，查onlineplay_onlineplay 表， 对应在线播放
def is_saved( href, table):
    global str_2_logfile
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='bdpan',charset='utf8')
    cursor=conn.cursor()

    if table == 1:
        sql_select = "SELECT * FROM movie_movie WHERE v_href='%s';" % href
    elif table == 2:
        sql_select = "SELECT * FROM onlineplay_onlineplay WHERE v_href='%s';" % href
    else:
        return 1

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
        f = codecs.open('/usr/bdpan_movie/daily/pandy/spider/autoSpider_log.txt', 'a', 'utf-8')
        # f = codecs.open('/home/lynn/github_project/daily/pandy/spider/autoSpider_log.txt', 'a', 'utf-8')
        for log in log_list:
            f.write(str(line_cnt) + ' ' + log + '\n')
            line_cnt += 1
        f.close()
    except:
        f = codecs.open('/usr/bdpan_movie/daily/pandy/spider/autoSpider_log_error.txt', 'a', 'utf-8')
        # f = codecs.open('/home/lynn/github_project/daily/pandy/spider/autoSpider_log_error.txt', 'a', 'utf-8')
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) )
        f.write('[write_2_logfile] write_2_logfile failed')
        f.write('\n\n\n')
        f.close()

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

    # 网盘资源
    # yeyoufang.com 爬虫
    yeyoufang = yeyoufang_Spider()
    title_list, url_list = yeyoufang.get_url()
    str_2_logfile.append('---------- yeyoufang 共有 %s 条数据需要插入 --------' % len(url_list))
    for detail_url in url_list:
        yeyoufang.get_info(detail_url)

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    # menggouwp 爬虫
    menggouwp = menggouwp_Spider()
    title_list, url_list = menggouwp.get_url()
    str_2_logfile.append('---------- menggouwp 共有 %s 条数据需要插入 --------' % len(url_list))
    for detail_url in url_list:
        menggouwp.get_info(detail_url)

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    # online resources
    kuyunzy = kuyunzy_Spider()
    title_list, url_list = kuyunzy.get_url()
    str_2_logfile.append('---------- kuyunzy 共有 %s 条数据需要插入 --------' % len(url_list))
    kuyunzy_cnt = 0
    for detail_url in url_list:
        kuyunzy.get_info(detail_url, title_list[kuyunzy_cnt])
        kuyunzy_cnt += 1
        write_2_logfile(str_2_logfile)
        str_2_logfile = []

    write_2_logfile(str_2_logfile)
    str_2_logfile = []

    # xujiating.cn 罗拉电影
    xujiating = xujiating_Spider()
    xujiating.get_info()

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
