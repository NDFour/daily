# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-08-19 13:03:37
# Last Modified: 2018-10-13 12:32:33
#

from werobot import WeRoBot
import pymysql
import re
import os
import configparser

robot=WeRoBot(token='wxtnt1024lynn')
robot.config['SESSION_STORAGE'] = False

### global isdebugi TO JUDGE IF THE PROGRAM IS IN DEBUG (test account)
# 0 > 一起来电影; 1 > NDFour登录的测试号；2 > 电影资源搜
isdebug=1

#global adtuple[] 用来存放小说数据，不用每次收到消息都访问数据库
adtuple=[]
adtuple2=[]

# adarticles_state 用来标识是否在该位置插入adarticles
ad1_state=1
ad2_state=1

# global reply_info_state 用来标识回复用户信息所需要调用的方法函数
reply_info_state=1

# baseUrl 构造search页链接
# 在线播放
baseUrl1='http://tnt1024.com/movie/search/?movie_name='
# 百度网盘 链接
baseUrl2='http://tnt1024.com/movie/search/?movie_name='

@robot.subscribe
def subscribe(message):
    #msg="注意：\n1  发送电影名字的时候请不要带其他特殊符号，只要电影名字即可；\n2  电影名字中请不要出现错别字"
    global adtuple
    global adtuple2
    outlist=[]
    outlist.append(['公众号免费看电影教程','','https://s1.ax1x.com/2018/06/02/CogADx.png','https://w.url.cn/s/AGW9n4L'])
    if adtuple:
        if ad1_state:
            outlist.append(adtuple)
    if adtuple2:
        if ad2_state:
            outlist.append(adtuple2)
    return outlist

# 用户取关
@robot.unsubscribe
def unsubscribe(message):
    #global last_movie
    pass
    # print('有用户取关啦！！！上一条消息是：[%s]'%last_movie)

# ViewEvent
@robot.view
def responsd_viewevent(message):
    return ''

@robot.text
def hello(message):
    #    return '        【系统升级】\n\n  公众号系统进行服务升级，预计24小时内完成。\n  请耐心等待升级完成！'

    #   the account of 'Lynn'
    master_root='o2NddxHhZloQV55azmx8zVXv9mAQ'
    if isdebug==1:
        master_root='ozDqGwZ__sjgDwZ2yRfusI84XeAc'
    elif isdebug==2:
        master_root='onD430y7UUrFB8sDV6W8PU4Skwy8'

    # reply_info() 函数调用标识
    global reply_info_state

    # 从'config.ini'文件中读取配置项
    loadConfigMsg=loadConfig()

    if message.source==master_root:
        #   预留adarticles添加接口，发送'insertadarticles .*',执行sql语句插入adarticles
        if re.match(r'insertadarticles .*',message.content):
            return insertadarticles(message.content)

        #   切换 articles 构造方式
        elif re.match(r'switch [0-9]',message.content):
            reply_info_state=int(message.content[7])
            # 写入到配置文件中，下次启动程序时自动加载
            msgWriteToConfigFile=writeToConfigFile('reply_info_state',str(reply_info_state))
            return msgWriteToConfigFile

        #   决定adarticles的开启状态
        elif re.match(r'ad1change [0-9]',message.content):
            global ad1_state
            ad1_state=int(message.content[10])
            # 写入到配置文件中，下次启动程序时自动加载
            msgWriteToConfigFile=writeToConfigFile('ad1_state',str(ad1_state))
            return msgWriteToConfigFile+'\nNow the ad1_state is : %s'%str(ad1_state)
        elif re.match(r'ad2change [0-9]',message.content):
            global ad2_state
            ad2_state=int(message.content[10])
            # 写入到配置文件中，下次启动程序时自动加载
            msgWriteToConfigFile=writeToConfigFile('ad2_state',str(ad2_state))
            return msgWriteToConfigFile+'\nNow the ad2_state is : %s'%str(ad2_state)

        # 更改 reply_info_bygenurl 中 在线观看 的 baseUrl1
        elif re.match(r'changebaseurl1 .*',message.content):
            global baseUrl1
            baseUrl1=message.content[15:]
            msgWriteToConfigFile=writeToConfigFile('baseUrl1',baseUrl1)
            return msgWriteToConfigFile+'\n更改 baseUrl1 成功!'

        # 更改 reply_info_bygenurl 中 网盘链接 的 baseUrl2
        elif re.match(r'changebaseurl2 .*',message.content):
            global baseUrl2
            baseUrl2=message.content[15:]
            msgWriteToConfigFile=writeToConfigFile('baseUrl2',baseUrl2)
            return msgWriteToConfigFile+'\n更改 baseUrl2 成功!'

        # 返回程序配置文件config.ini中相关配置
        elif message.content=='showConfig':
            msg=showConfig()
            return msg

    # print('《%s》'%message.content)
    v_name=message.content

    if(len(v_name) > 30):
        return '电影名长度过长，请精简关键字后重新发送。'

    v_name=modefy_name(v_name)

    # 调用 reply_info(), 控制 articles 生成方式
    if reply_info_state==1:
        articles=reply_info(v_name)
    elif reply_info_state==2:
        articles=reply_info_bygenurl(v_name)

    a = []
    a.append(articles[0])
    return a

# 替换用户发来的电影名字中的错别字
def modefy_name(v_name):
    # 先把电影名字中的特殊符号去除
    v_name=v_name.replace('《','')
    v_name=v_name.replace('》','')
    v_name=v_name.replace('。','')

    return v_name

# 通过查询数据库将结果返回给用户
def reply_info(v_name):
    #   递归调用时，如电影名为空，直接返回
    if v_name == '':
        return '数据库中暂无该影片，请先观看其他影片。\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。'

    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    try:
        sql_select="SELECT name,videourl,picurl FROM weixunmi WHERE name LIKE '%v_name%';"
        sql_select=sql_select.replace('v_name',v_name)
        cursor.execute(sql_select)

        out_list=[]
        cnt=0

        for i in cursor.fetchmany(6):
            in_list=[]
            in_list.append(i[0])
            in_list.append(i[0])
            in_list.append(i[1])
            in_list.append(i[2])
            # in_list.append(i[1].replace('fiml','player').replace('.html','-1-1.html').replace('18.19.ivdmh','wx.wx18.lcdoor'))

            out_list.append(in_list)
            cnt+=1
    except:
        cursor.close()
        conn.close()
        return '查询数据失败，错误代码 0x_reply_info_().SELECT ERROR\n\n-想让你的公众号也具有发送名字即可在线观看电影功能？\n-欢迎加我微信 ndfour001 洽谈合作。 '

    len_v_name=len(v_name)
    #   如果搜索不到数据，则将电影关键词长度一再缩小
    while ((cnt == 0) and len_v_name):
        len_v_name-=1
        # 调用递归之前关闭本层数据库链接
        cursor.close()
        conn.close()
        return reply_info(v_name[0:len_v_name])

    #   图文消息加上之前的广告推文链接
    global adtuple
    global adtuple2
    global ad1_state
    global ad2_state
    if ad2_state:
        if adtuple2:
            out_list.insert(1,adtuple2)
    if ad1_state:
        if adtuple:
            if cnt>2:
                out_list.insert(4,adtuple)
            else:
                out_list.append(adtuple)

    # 关闭数据库链接
    cursor.close()
    conn.close()

    if int(cnt)<6:
        out_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])

    return out_list

# 构造查询 url 返回给用户
def reply_info_bygenurl(v_name):
    out_list=[]

    # 在线搜索 URL
    #baseUrl='http://m.nemfh.cn/index.php/home/index/search.html?k='
    global baseUrl1
    url = baseUrl1 + v_name + '&onlineplay_search=onlineplay_search'
    name='【在线观看】《'+v_name+'》'
    # picurl='https://s1.ax1x.com/2018/08/11/P6L2sU.jpg'
    picurl = 'http://wx1.sinaimg.cn/mw690/0060lm7Tly1fuh4pci3jjj30p00dwgmc.jpg'
    # 插入搜索词条链接图文消息
    in_list=[]
    in_list.append(name)
    in_list.append(name)
    in_list.append(picurl)
    in_list.append(url)
    out_list.append(in_list)

    # 网盘电影网站 搜索结果
    in_list=[]
    name_pan='【网盘资源】《' + v_name + '》'
    global baseUrl2
    # pic_pan='https://upload-images.jianshu.io/upload_images/5649568-867870961e0b81c5.jpg'
    pic_pan = 'http://wx1.sinaimg.cn/mw690/0060lm7Tly1fuh4pci3jjj30p00dwgmc.jpg'
    url_pan=baseUrl2 + v_name + '&movie_search=movie_search'
    in_list.append(name_pan)
    in_list.append(name_pan)
    in_list.append(pic_pan)
    in_list.append(url_pan)
    out_list.append(in_list)

    #   图文消息加上一条之前的广告推文链接
    global adtuple
    global adtuple2
    global ad1_state
    global ad2_state
    if ad1_state:
        if adtuple:
            out_list.append(adtuple)
    if ad2_state:
        if adtuple2:
            out_list.append(adtuple2)
    # 插入查电影服务推广图文
    # out_list.append(['想让你的公众号也可以查电影？点我','想让你的公众号也可以查电影？点我','https://t1.picb.cc/uploads/2018/03/14/22PY0u.png','http://kks.me/a4Y9N'])
    # 插入“视频无法播放”
    # out_list.append(['如果无法播放点我查看教程','','https://t1.picb.cc/uploads/2018/01/27/Lz2KR.png','http://t.cn/R8hJGC7'])

    # 插入点广告文章
    # 当ad1或者ad2至少存在一个时才会插入该文章
    if ad1_state+ad2_state:
        out_list.append(['■ 亲爱的，每天看电影时帮我点一下上面的小说呗','','https://t1.picb.cc/uploads/2018/05/21/2azICG.jpg','https://w.url.cn/s/ARlJPBS'])
    return out_list

def insertadarticles(message_content):
    # DEMO: inertadarticles INERT INTO adarticles(title,picurl,url,canbeuse) VALUES ('**','**','**',1);

    # 插入小说数据
    sql_insert=message_content.replace('insertadarticles ','')
    # 更新小说数据全局变量
    ad_select="SELECT title,picurl,url FROM adarticles Where canbeuse=1 AND tab=1 ORDER BY id DESC"
    ad_select2="SELECT title,picurl,url FROM adarticles Where canbeuse=1 AND tab=2 ORDER BY id DESC"
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='cqmygpython2',db='wechatmovie',charset='utf8')
    cursor=conn.cursor()

    # 插入小说数据
    try:
        cursor.execute(sql_insert)
        conn.commit()
        msg = '成功插入一条【广告图文】到数据库！'
    except:
        conn.rollback()
        msg = '插入一条【广告图文】到数据库失败！'

    # 更新adarticles全局变量
    global adtuple
    global adtuple2
    adtuple=[]
    adtuple2=[]
    try:
        cursor.execute(ad_select)
        adarticles_list=cursor.fetchone()
        if adarticles_list:
            adtuple.append(adarticles_list[0])
            adtuple.append(adarticles_list[0])
            adtuple.append(adarticles_list[1])
            adtuple.append(adarticles_list[2])
        # 添加第二条数据
        cursor.execute(ad_select2)
        adarticles_list=cursor.fetchone()
        if adarticles_list:
            adtuple2.append(adarticles_list[0])
            adtuple2.append(adarticles_list[0])
            adtuple2.append(adarticles_list[1])
            adtuple2.append(adarticles_list[2])

        msg+='\n更新 adarticles 全局变量成功！'
    except:
        msg+='\n更新 adarticles 全局变量失败！'
    finally:
        cursor.close()
        conn.close()

    return msg

# 返回程序配置文件中相关配置项
def showConfig():
    global ad1_state
    global ad2_state
    global reply_info_state
    global baseUrl1
    global baseUrl2

    msg='config.ini:\n'
    msg+='\nad1_state:'+str(ad1_state)
    msg+='\nad2_state:'+str(ad2_state)
    msg+='\nreply_info_state:'+str(reply_info_state)
    msg+='\nbaseUrl1:'+baseUrl1
    msg+='\nbaseUrl2:'+baseUrl2

    return msg

# 从'config.ini'文件中读取程序配置参数
def loadConfig():
    global ad1_state
    global ad2_state
    global reply_info_state
    global baseUrl1
    global baseUrl2

    config=configparser.ConfigParser()
    config.read("config.ini")

    # 各位置adarticles状态开关
    try:
        ad1_state=config.getint('werobot','ad1_state')
        ad2_state=config.getint('werobot','ad2_state')
        # global reply_info_state 用来标识回复用户信息所需要调用的方法函数
        reply_info_state=config.getint('werobot','reply_info_state')
        # baseUrl 构造search页链接
        baseUrl1=config.get('werobot','baseUrl1')
        baseUrl2=config.get('werobot','baseUrl2')
    except:
        return 'config.ini配置文件加载失败'

    return 'config.ini配置文件加载完毕'

# 接受两个参数 ： 配置项名称、配置项的值
def writeToConfigFile(configName,configValue):
    config=configparser.ConfigParser()
    config.read('config.ini')
    try:
        config.set('werobot',configName,configValue)
        config.write(open('config.ini','w'))
    except:
        return '写入 %s 到配置文件 config.ini 时失败' % configName
    return '写入 %s 到配置文件 config.ini 成功' % configName
