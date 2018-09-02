# -*- coding:utf-8 -*-
#   Description: 本程序爬取电影信息并存储到数据库用于 tnt1024.com 站点使用
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-08-30 11:18:12
# Last Modified: 2018-08-30 19:31:37
#

import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import pymysql
import time
import os
import traceback

class movieSpider:
    # 采集网站的目录url
    category_urls = [
            'http://www.menggouwp.com/a/dianying/list_1_',
            ]
    # 每次需要更新的页数+1
    pages_num = 2

    def __init__(self):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print('\tmovieSpider for yeyoufang.com')
        print()
        print('>> movieSpider init...')

        # 关闭 django 应用 pandy
        print('>> stop [pandy]')

        print('\n\n')

    # 遍历目录获取电影名保存到列表，删除已存在数据库的，然后获取电影信息
    # 返回值： 1-电影名列表 2-电影详情页url列表 （返回的均为数据库中不存在的)
    def get_url(self):
        current_page = 1
        movies_num = 0
        # 以下两个列表用于返回
        title_list = []
        url_list = []

        for category in self.category_urls:
            # 遍历 pages_num 页
            while current_page < self.pages_num:
                print('>> [get_url] now is page %s\n>> %s\n' % (current_page, category + str(current_page) + '.html' ) )
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
                    if self.is_saved(title, 'http://www.menggouwp.com'+href):
                        # print('>> [get_url] skip already exsist\n  %s' % title)
                        print('>> [get_url] already exsist')
                        url_cnt += 1
                    else:
                        url_list.append(href)
                        title_list.append(title)
                        url_cnt += 1

                # 页码数 ++ ，构造下一页的目录页url
                current_page += 1

        print('>> [get_url] total %s movies' % movies_num)
        return title_list,url_list

    # 解析详情页获得电影信息，返回电影信息 列表
    def get_info(self, detail_url):
        print('>> [get_info] %s' % detail_url)

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

    # 判断传入的 影片名 是否已存在于数据库
    def is_saved(self, title, href):
        conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='bdpan',charset='utf8')
        cursor=conn.cursor()

        sql_select = "SELECT * FROM movie_movie WHERE v_href='%s';" % href
        try:
            cursor.execute(sql_select)
        except:
            pass
        finally:
            cursor.close()
            conn.close()

        target_num = len(cursor.fetchall())

        if target_num != 0:
            return 1
        return 0

    # 接收传入的电影信息作为参数 构造并执行sql 保存数据至db，保存新数据的同时删除旧数据
    # 接收参数： sql_param : 影片的信息
    def save_2_db(self, sql_param):
        # sql_param: name, pic, text_info, bdpan, pass, href
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='cqmygpython2', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql_insert = 'INSERT INTO movie_movie(v_name, v_pic, v_text_info, v_bdpan, v_pass, v_href, v_pub_date, v_ed2k, v_magnet, v_ed2k_name, v_magnet_name, v_valid, v_views) VALUES ("%s", "%s", "%s", "%s", "%s",  "%s", "%s", "%s", "%s", "%s", "%s", 1, 0);' % \
        (sql_param[0], sql_param[1], sql_param[2], sql_param[3], sql_param[4], sql_param[5], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '', '', '', '')

        try:
            cursor.execute(sql_insert)
            conn.commit()
            print('>> [save_2_db] insert succes')

            # 检测数据库中是否有和该电影采集页url一致 但是 电影名 不一样（旧版）的，有的话删除
            movie_name = sql_param[0]
            movie_href = sql_param[5]
            sql_del = 'DELETE FROM movie_movie WHERE v_href="%s" AND v_name!="%s";' % (movie_href, movie_name)
            try:
                cursor.execute(sql_del)
                conn.commit()
                print('>> [save_2_db] del old version success\n')
            except:
                conn.rollback()
                print('>> [save_2_db] del old version failed\n')
        except:
            conn.rollback()
            print('>> [save_2_db] insert failed')

        cursor.close()
        conn.close()

    # 统计本次 蜘蛛 运行情况，发送邮件报告
    def send_mail(self):
        pass

    # 获取网页文本
    def get_html(self,url):
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
            print('>> [get_html] success %s' %len(html_text))
        except Exception as e:
            html_text = ''
            print('>> [get_html] failed')
            print(e.traceback())
        return html_text


def main():
    spider = movieSpider()
    # 获取目录中的需要爬取的新电影名和详情页url 列表
    title_list,url_list = spider.get_url()

    # 获取详情页电影信息
    for detail_url in url_list:
        spider.get_info(detail_url)
    # spider.get_info('http://www.yeyoufang.com/33081.htm')

main()
