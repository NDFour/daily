# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-08-29 19:41:00
# Last Modified: 2018-08-30 10:50:14
#

import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import time

class html2pdf(object):
    def __init__(self):
        print('> html2pdf is running...')
        print()
        self.get_urls()

    def get_urls(self):
        urls  = []
        url_cnt = 0
        init_num = int(input('Begin with ?'))
        with open('urls', 'r') as f:
            for url in f.readlines():
                if url_cnt >= init_num:
                    urls.append('https://liaoxuefeng.com' + url[0:-2])
                url_cnt += 1

        print('>> 共有 %s 条urls' %len(urls))
        self.save_html(urls, init_num)

    def save_html(self,urls, init_num):
        htmls = []
        html_cnt = 0
        html_cnt = init_num

        headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'widget.weibo.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

        for url in urls:
            r = requests.get(url, headers=headers, timeout=6)
            r.encoding =  r.apparent_encoding

            # 得到章节标题
            page_title_re = re.compile(r'<h4>.*</h4>')
            page_title = page_title_re.findall(r.text)[0].replace('h4','h1')

            # 只解析部分网页，节约服务器内存和带宽
            only_content_main = SoupStrainer(class_="x-wiki-content x-main-content")
            soup = BeautifulSoup(r.text, 'lxml', parse_only = only_content_main)

            html_file_name = 'htmls/%s.html' % str(html_cnt)

            with open (html_file_name, 'w') as f:
                print('> saving [%s]' % url)
                html_text = '<meta charset="utf-8" />' + page_title + soup.prettify()
                f.write( html_text )
                htmls.append(html_file_name)
                html_cnt += 1
                print('>> [%s] %s saved.' % (html_cnt-1, html_file_name))
                print()

def main():
    h2pdf = html2pdf()

main()
