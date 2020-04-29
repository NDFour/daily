import requests
from bs4 import BeautifulSoup
import time
import csv

import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class ChenJin5_Spider():

    request_header = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }

    # 工作路径
    _path = ''
    # qq 群
    group_num = ''



    def __init__(self, _path, group_num):
        print('## Chenjin5_Spider init...')
        self._path = _path
        self.group_num = group_num

    # 用于 chenjin5.com 图书自动更新
    def auto_update(self):
        index_page = 'https://www.chenjin5.com/'
        return self.get_detail_url(index_page)


    # 从 主页/目录 中提取图书详情页 URL
    # url: 待解析的目录页
    def get_detail_url(self, url):
        soup = BeautifulSoup( self.get_html(url), 'lxml' )

        book_list = []
        book_cnt = 0
        for c in soup.select("div.thumbnail"):
            # 先判断该图书是否已存在数据库中
            detail_url = c.a['href']
            if is_crawled(detail_url, self._path):
                # print('^ 已爬取过')
                # print()
                continue
            else:
                # print('^ 未爬取过')
                mark_crawed(detail_url, self._path)
                # print()

            category = c.p.text.strip()
            author = c.div.select('p')[1].text.strip()
            title = c.div.a.text.strip()
            book_cnt += 1

            '''
            print(title)
            print(author)
            print(category)
            print(detail_url)
            print()
            '''

            detail_url = 'https://www.chenjin5.com' + detail_url
            book_item = {}
            book_item['标题'] = title
            book_item['作者'] = author
            book_item['分类'] = category
            book_item['免费下载链接'] = detail_url
            '''
            book_item['title'] = title
            book_item['author'] = author
            book_item['category'] = category
            book_item['detail_url'] = detail_url           
            '''
            book_list.append(book_item)

        return book_list



    # 请求网络 获取 html
    # url: 待请求的 URL
    def get_html(self, url):
        try:
            r = requests.get( url, headers = self.request_header, timeout = 30 )
            return r.text
        except Exception as e:
            print('get_html 出错')
            print(e)

            return 0


    # 写入记录到 csv
    def toCsv(self, book_list):
        _path = self._path
        file_name = str( time.strftime("%Y-%m-%d", time.localtime()) ) + '_Kindle电子书免费分享_群:' + self.group_num + '.csv'
        # 标记是否已 写入 header
        is_header = False
        # 写入 csv 文件 ; encoding 解决用 wps 打开后中文乱码
        with open(_path + file_name, 'a', encoding = 'utf-8-sig') as csvfile:
            fieldnames = [ '标题', '作者', '分类', '免费下载链接']
            # fieldnames = [ 'title', 'author', 'category', 'detail_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #注意header是个好东西
            if not is_header:
                writer.writeheader()
                is_header = True
            else:
                pass
            for u_items in book_list:
                # print(u_items)
                writer.writerow(u_items)

        return file_name


    # 展示已爬取到的 book_item
    def show_book_item(self):
        for book in self.book_item_list:
            print(book)
            print()


# 标记该图书已被爬取过
def mark_crawed(detail_url, _path):
    with open(_path + 'is_crawled.txt', 'a') as f:
        f.write(detail_url)
        f.write('\n')


# 判断该图书是否已存在于数据库中
def is_crawled(detail_url, _path):
    with open(_path + 'is_crawled.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() == detail_url:
                return True
    return False


# 删除发送后的附件
def del_attachment(full_path_filename):
    if len(full_path_filename):
        print('sleep 10s...')
        time.sleep(10)
        del_cmd = 'rm ' + full_path_filename
        os.system(del_cmd)
    else:
        print('No need to del')


# 推送消息到邮箱
def mailtestmsg(book_item_list, full_path_filename, file_name):
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 发邮件代码
    _user = "lgang219@qq.com"
    _pwd  = "xxxxxxxxxxxxxxxxx"
    _to   = "ndfour@foxmail.com"

    mail_content = '今日更新:\n\n'
    if len(book_item_list):
        mail_content += '共 ' + str(len(book_item_list)) + '\n\n'
        try:
            for book in book_item_list:
                mail_content += book['标题']
                mail_content += '\n'
                mail_content += book['作者']
                mail_content += '\n'
                mail_content += book['分类']
                mail_content += '\n'
                mail_content += book['免费下载链接']
                mail_content += '\n\n'
        except Exception as e:
            pass
    else:
        mail_content += '今日没有新内容'

    try:
        # msg = MIMEText( mail_content )
        msg = MIMEMultipart()
        msg["Subject"] = "[Kindle电子书免费分享_群] 日更提醒邮件"
        msg["From"] = _user
        msg["To"] = _to

        # 文本消息
        msg.attach(MIMEText(mail_content))

        # 添加附件
        if len(book_item_list):
            attachment = MIMEApplication( open(full_path_filename, 'rb').read() )
            attachment.add_header('Content-Disposition', 'attachment', filename = file_name )
            msg.attach( attachment )

        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
    except Exception as e:
        pass
    
    del_attachment(full_path_filename)




# 上传前移除发邮件密码
# 上传前移除发邮件密码
# 上传前移除发邮件密码

def main():
    # aibook
    chenjin5 = ChenJin5_Spider('/root/rootcron_tasks/chenjin5_daily_crawler/', 'xxxxxxx')
    book_list = chenjin5.auto_update()
    full_path_filename = ''
    if len(book_list):
        full_path_filename = chenjin5.toCsv(book_list)

    mailtestmsg(book_list, full_path_filename, full_path_filename.split('/')[-1])

    # mailtestmsg()


main()
