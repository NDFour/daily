#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-04-22 10:40:47
# Last Modified: 2018-07-16 22:16:20
#

import re
import requests

def getHtml(url):
    try:
        r=requests.get(url)
        return r.text 
    except:
        return ''

def findTitle(html_text):
    title_re=re.compile(r'<title>\n.*')
    title=''
    try:
        title_raw=title_re.findall(html_text)
        title=title_raw[0].replace('<title>','').replace('\n','').replace(' ','').replace('\t','')
        title='【推荐】'+title
    except:
        title='未找到 title'
    return title

def findPic(html_text):
    pic_re=re.compile(r'msg_cdn_url = .*')
    pic=''
    try:
        pic_raw=pic_re.findall(html_text)
        pic_raw=pic_raw[0]
        pic=pic_raw.replace('msg_cdn_url = "','').replace('";','')
    except:
        pic='未找到 pic'
    return pic

def findAdPic(html_text):
    pic_re=re.compile(r'<img data-src="https.*?"')
    pic=''
    try:
        pic_raw=pic_re.findall(html_text)
        pic_raw=pic_raw[0]
        pic=pic_raw.replace('<img data-','')
    except:
        pic='未找到 pic2'
    return pic

def getSql(title,url,pic):
    sql_raw='insertadarticles INSERT INTO adarticles(title,picurl,url,canbeuse,tab) VALUES ( "▉ title_sql","pic_sql" ,"url_sql" ,1, 1);'

    sql_insert=sql_raw.replace('title_sql',title).replace('url_sql',url).replace('pic_sql',pic)
    return sql_insert


def main():
    print("------------insertADArticles.py--------------")
    url=input("Please input the url of the article:\n")

    html_text=getHtml(url)

    title=findTitle(html_text)
    pic=findPic(html_text)
    pic2=findAdPic(html_text)

    insert_sql=getSql(title,url,pic)
    insert_sql2=getSql(title,url,pic2)

    print('>> Pic:')
    print(insert_sql)
    print()
    print('>> Pic 2:')
    print()
    print(insert_sql2)

    '''
    print()
    print('title')
    print(title)
    print()
    print('pic')
    print(pic)
    print()
    print('pic 2')
    print(pic2)
    print()
    '''


main()
