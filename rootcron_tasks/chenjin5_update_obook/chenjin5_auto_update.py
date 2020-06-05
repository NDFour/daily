import requests
from bs4 import BeautifulSoup
import time
import csv

import pymysql

import smtplib
from email.mime.text import MIMEText


class OBooks_Spider():

    request_header = {
    'authority': 'www.obook.cc', 
    'method': 'GET',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    }


    # 图书详情页 URL 列表
    book_detail_list = []
    # 生成的 图书对象 列表
    book_item_list = []
    # 生成 csv 文件
    title_list = ['title', 'author', 'rating', 'category', 'infos', 'pic',
    'pan_1', 'pan_2', 'pan_3', 'pan_pass', 'origin']


    def __init__(self):
        print('## OBooks_Spider init...')
        self.s_session = requests.Session()
        # 模拟登录


    # 模拟登录
    def _login(self):
        form_data = {
            'email': 'seend',
            'password': 'aa4d74090a61febb3465c13966148a86',
        }
        self.s_session.post('https://www.obook.cc/user-login.htm', data = form_data, timeout = 30)
        # 验证是否登陆成功
        '''
        r = self.s_session.get('https://www.obook.cc/my.htm', timeout = 30)
        with open('my.html', 'w') as f:
            f.write(r.text)
        '''


    # 模拟登出
    def _logout(self):
        r = self.s_session.get('https://www.obook.cc/user-logout.htm', timeout = 30)
        # 验证是否登出 成功
        '''
        with open('logout.html', 'w') as f:
            f.write(r.text)
        '''


    # 用于 chenjin5.com 图书自动更新
    def auto_update(self):
        index_page = 'https://www.obook.cc'
        self.get_detail_url(index_page)


    # 从 主页/目录 中提取图书详情页 URL
    # url: 待解析的目录页
    def get_detail_url(self, url):
        soup = BeautifulSoup( self.get_html(url), 'lxml' )
        book_cnt = 0
        for c in soup.select("li.thread"):
            # 先判断该图书是否已存在数据库中
            print(c.a['href'])
            if is_crawled('https://www.obook.cc/' + c.a['href']):
                print('^ 已爬取过')
                print()
                continue
            else:
                print('^ 未爬取过')
                print()
            # self.book_detail_list.append( c.h3.a['href'] )
            # 分类
            category = '其它'
            try:
                category = self.convert_category( c.select('a.badge')[0].text.strip() )
            except Exception as e:
                print('获取 category 失败')
                category = '其它'
            # 作者
            # author = c.p.text[3:].strip()
            author = '请参考图书详情'
            # 豆瓣评分
            # rating = c.font.text.strip()
            rating = '0.0'
            # 解析详情页
            self.parse_detail( c.a['href'], author, rating, category )
            book_cnt += 1


    # 将从本网站提取到的 category 转换成 chenjin5 专用
    def convert_category(self, category):
        category_dic = {
            '小说': '小说文学',
            '绘本': '小说文学',
            '文学': '小说文学',
            '随笔': '小说文学',

            '社科': '人文社科',
            '宗教': '人文社科',
            '文化': '人文社科',
            '哲学': '人文社科',
            '心理': '人文社科',
            '艺术': '人文社科',

            '成长': '励志成功',

            '历史': '历史传记',
            '传记': '历史传记',

            '科普': '学习教育',
            '教育': '学习教育',
            '法律': '学习教育',

            '生活': '生活时尚',
            '婚恋': '生活时尚',
            '商业': '经济管理',
            '管理': '经济管理',
            '理财': '经济管理',

            '经济金融': '经济管理',

            '互联网': '编程开发',

            '合集': '其它',
        }

        try:
            rel = category_dic[category]
        except Exception as e:
            rel = '其它'

        # print('-> convert_category:' + category + ' -> ' + rel)

        return rel


    # 解析详情页的各种图书信息
    # url: 待解析的详情页
    def parse_detail(self, url, author, rating, category):
        # for d_url in self.get_detail_url:
        d_url = 'https://www.obook.cc/' + url 
        # print()
        # print('开始解析：' + d_url)

        soup = BeautifulSoup( self.get_html(d_url), 'lxml' )
        book_content = soup.select("div.card-thread")[0].div

        title = self.extract_title(book_content)
        if not title:
            return

        # 图书 作者 简介 等信息
        infos = self.extract_infos(book_content)

        # 内容简介
        description = self.extract_description(book_content)

        # 图书封面
        pic = self.extract_pic(book_content)

        # 图书 网盘链接
        pan_1 = self.extract_pan_1(book_content)
        pan_2 = self.extract_pan_2(book_content)
        pan_3 = self.extract_pan_3(book_content)
        len_pan = len(pan_1) + len(pan_2) + len(pan_3)
        if not len_pan:
            print('一个网盘链接都没有找到，跳过')
            return

        # 图书 网盘 提取码
        pan_pass = self.extract_pan_pass(book_content)

        # 生成 书籍对象
        book_item = self.gen_book_item(title, author, rating, category, infos, description, pic, pan_1, pan_2, pan_3, pan_pass, d_url)
        self.book_item_list.append(book_item)

        time.sleep(3)


    # 从详情页 提取 title
    def extract_title(self, book_content):
        title = ''
        try:
            title = book_content.div.div.h4.text.strip()
            title = ' '.join(title.split())
            print(title)
        except Exception as e:
            print('爬取 title 失败')
            print(e)
        return title

    # 从详情页 提取 infos
    def extract_infos(self, book_content):
        return '暂无'

    # 从详情页 提取 description
    def extract_description(self, book_content):
        description = ''
        try:
            description = book_content.select("div#hide-line")[0].text
        except Exception as e:
            print('爬取 description 失败')
            print(e)
            print('########### description')
        return description

    # 从详情页 提取 pic
    def extract_pic(self, book_content):
        pic = ''
        try:
            pic = book_content.select("div.message")[0].img['src']
        except Exception as e:
            print('爬取 pic 失败')
            print(e)
            print('########### pic')
        return pic

    # 从详情页 提取 pan_1
    def extract_pan_1(self, book_content):
        pan_1 = ''
        try:
            pan_1 = book_content.select('fieldset')[0].td.text + '##' + book_content.select('fieldset')[0].td.a['href']
        except Exception as e:
            print('爬取 pan_1 失败')
            # print(e)
        return pan_1

    # 从详情页 提取 pan_2
    def extract_pan_2(self, book_content):
        pan_2 = ''
        try:
            pan_2 = book_content.select('fieldset')[1].td.text + '##' + book_content.select('fieldset')[1].td.a['href']
        except Exception as e:
            print('爬取 pan_2 失败')
            # print(e)
        return pan_2

    # 从详情页 提取 pan_3
    def extract_pan_3(self, book_content):
        pan_3 = ''
        try:
            pan_3 = book_content.select('fieldset')[2].td.text + '##' + book_content.select('fieldset')[2].td.a['href']
        except Exception as e:
            print('爬取 pan_3 失败')
            # print(e)
        return pan_3

    # 从详情页 提取 pan_pass
    def extract_pan_pass(self, book_content):
        pan_pass_1 = ''
        try:
            pan_pass_1 = book_content.select('fieldset')[0].tbody.text + '：' + book_content.select('fieldset')[0].tbody.input['value']
        except Exception as e:
            print(e)

        pan_pass_2 = ''
        try:
            pan_pass_2 = book_content.select('fieldset')[1].tbody.text + '：' + book_content.select('fieldset')[1].tbody.input['value']
        except Exception as e:
            print(e)

        pan_pass_3 = ''
        try:
            pan_pass_3 = book_content.select('fieldset')[2].tbody.text + '：' + book_content.select('fieldset')[2].tbody.input['value']
        except Exception as e:
            print(e)
            
            
        return pan_pass_1 + '\n' + pan_pass_2 + '\n' + pan_pass_3



    # 生成 book对象 字典，方便调用
    def gen_book_item(self, title, author, rating, category, infos, description, pic, pan_1, pan_2, pan_3, pan_pass, origin):
        book_i = {
            'title': title,
            'author': author,
            'rating': rating,
            'category': category,
            'infos': infos,
            'description': description,
            'pic': pic,
            'pan_1': pan_1,
            'pan_2': pan_2,
            'pan_3': pan_3,
            'pan_pass': pan_pass,
            'origin': origin,
        }

        return book_i


    # 请求网络 获取 html
    # url: 待请求的 URL
    def get_html(self, url):
        try:
            r = self.s_session.get( url, timeout = 30 )
            return r.text
        except Exception as e:
            print('get_html 出错')
            print(e)

            return 0

    # 展示已爬取到的 book_item
    def show_book_item(self):
        for book in self.book_item_list:
            print(book)
            print()



# 判断该图书是否已存在于数据库中
def is_crawled(origin_url):
    conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='xqksj', db='bdpan', charset='utf8')
    cursor = conn.cursor()

    sql_cmd = 'select id from books_books where book_origin="' + origin_url + '";'

    rel_cnt = cursor.execute(sql_cmd)
    if rel_cnt:
        return True
    else:
        return False


# 将爬取到的数据存储到数据库
def save_2_db( sql_list ):
    conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='xqksj', db='bdpan', charset='utf8')
    cursor = conn.cursor()

    succ_cnt = 0
    fail_cnt = 0
    for i in sql_list:
        try:
            cursor.execute(i)
            conn.commit()
            succ_cnt += 1
        except:
            conn.rollback()
            fail_cnt += 1
    cursor.close()
    conn.close()

    print('succ_cnt:' + str(succ_cnt))
    print('fail_cnt:' + str(fail_cnt))


# 生成 插入 book_item 的 sql 语句
# 将 self.book_list[] 中的所有 book item 都转化为 sql 插入语句，并放在 self.sql_list[]
def gen_sql( book_list ):
    sql_list = []
    for book in book_list:
        sql_base = 'INSERT INTO books_books ( book_title, book_pic, book_author, book_category, book_infos, book_description, book_origin, book_pan_1, book_pan_2, book_pan_3, book_pan_pass, book_rating, book_valid, book_views, book_pub_date) VALUES ('
        sql_base += '"' + book['title'] + '", '
        sql_base += '"' + book['pic'] + '", '
        sql_base += '"' + book['author'] + '", '
        sql_base += '"' + book['category'] + '", '
        sql_base += '"' + book['infos'] + '", '
        sql_base += '"' + book['description'] + '", '
        sql_base += '"' + book['origin'] + '", '
        sql_base += '"' + book['pan_1'] + '", '
        sql_base += '"' + book['pan_2'] + '", '
        sql_base += '"' + book['pan_3'] + '", '
        sql_base += '"' + book['pan_pass'] + '", '
        sql_base += '"' + book['rating'] + '", '
        sql_base += '1, '
        sql_base += '0, '
        sql_base += '"' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() ) + '");'

        sql_list.append(sql_base)

    return sql_list


# 推送消息到邮箱
def mailtestmsg(book_item_list):
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 发邮件代码
    _user = "lgang219@qq.com"
    _pwd  = "xxxxxxxxxx"
    _to   = "ndfour@foxmail.com"

    mail_content = '今日更新:\n\n'
    if len(book_item_list):
        try:
            for book in book_item_list:
                mail_content += book['title']
                mail_content += '\n'
                mail_content += book['category']
                mail_content += '\n'
                mail_content += book['origin']
                mail_content += '\n\n'
        except Exception as e:
            pass
    else:
        mail_content += '今日没有新内容'
    msg = MIMEText( mail_content )
    msg["Subject"] = "[chenjin5 Auto Update] 日更提醒邮件"
    msg["From"] = _user
    msg["To"] = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
    except Exception as e:
        pass




# 上传前移除发邮件密码
# 上传前移除发邮件密码
# 上传前移除发邮件密码

def main():
    # obook
    obook = OBooks_Spider()
    obook._login()
    obook.auto_update()
    # obook.show_book_item()
    sql_list = gen_sql(obook.book_item_list)
    save_2_db(sql_list)
    obook._logout()

    mailtestmsg(obook.book_item_list)

    '''
    with open('sql.txt', 'a') as f:
        for sql in sql_list:
            f.write(sql)
            f.write('\n')
            f.write('\n')
    '''


main()
