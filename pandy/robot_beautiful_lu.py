# -*- coding: utf-8 -*-

from werobot import WeRoBot
import re
import configparser
import sqlite3
import time
import traceback


robot_beautiful_lu = WeRoBot(token='beautiful_lu')
robot_beautiful_lu.config['SESSION_STORAGE'] = False


# 显示帮助菜单
def show_help():
    rel = '【帮助菜单】\n'
    rel += '- - - - - - - - - - - - - - - - - -\n\n'
    rel += 'help —显示帮助菜单\n\n'
    rel += 'cx xxoo —查询名为 "xxoo" 的影片\n\n'
    rel += 'get 1234 —获得 ID 为 1234 的影片的下载链接\n\n'

    rel += 'aw 100.01 —添加体重记录 100.01(斤）\n\n'
    rel += 'cw —查询体重记录'

    return rel


@robot_beautiful_lu.subscribe
def subscribe(message):
    return '是卢大漂亮来了么？[奸笑][奸笑]'


@robot_beautiful_lu.text
def hello(message):
    db_name = 'gaoqing_fm_2021_1_8.sqlite3'

    str_input = message.content.strip()
    # str_input = message.strip()

    msg = ''

    if str_input == 'help':
        msg = show_help()
    elif str_input == 'cw':
        msg = '查询体重记录（功能建设中。。。)'
    else:
        try:
            cmds = str_input.split(' ')[:2]

            # 查询电影
            if cmds[0] == 'cx':
                m_name = cmds[1].strip().replace('《', '').replace('》', '')
                msg = get_rel(m_name, db_name)
            # 获得电影下载链接
            elif cmds[0] == 'get':
                # 根据 ID 搜索 详情
                msg = get_by_id(int(cmds[1].strip()), db_name)
            # 添加体重记录
            elif cmds[0] == 'aw':
                msg = '添加体重记录 （功能建设中。。。）'

            else:
                msg = '快检查一下是不是命令用错啦！识别不鸟🐦 ～\n\n发送 help 查看命令用法'
        except Exception as e:
            traceback.print_exc()
            msg = str(e)
            msg += '\n\n⚠️ 出现错误啦！\n快把这条消息复制发给小刚刚管理员 👮‍♀️'

    return msg


def get_rel(name, db_name):
    # 回复给用户的消息体
    msg = ''
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        sql = "select id,name from movies where name" + " like '%" + name + "%' order by length(name) limit 15"
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()[:30]

        '''
        搜索「城南旧事」的结果,
        发送前面编码获得网盘，注册用户直接点击书名查看
        - - - - - - - - - - - - - - - - - - 
        [ 103704 ]城南旧事
        [ 112760 ]城南旧事
        [ 114159 ]城南旧事
        - - - - - - - - - - - - - - - - - - 
        ◎ 参加辣豆瓣每天读书5分钟打卡
        ◎ 查看书单，发送数字 3 
        ◎ 加入书友群求助书友。
        '''

        if len(rel):
            msg = '搜索 《' + name + '》 的结果，\n发送 get + 前面编码获得磁力🧲链接。\n\n- - - - - - - - - - - - - - - - - - \n'
            for m in rel:
                msg += '[ ' + str(m[0]) + ' ]' + m[1] + '\n'
            msg += '\n- - - - - - - - - - - - - - - - - - \n'
            msg += '⚠️ 名字可以不完整，但是一定不要有错别字哦 ~'

        else:
            msg = '你好，没有找到跟《' + name + '》相符合的电影哦\n你可以换一个电影试试~~~'
    except Exception as e:
        # print(e)
        msg = '你好，没有找到跟《' + name + '》相符合的电影哦\n你可以换一个电影试试~~~'
    finally:
        cursor.close()
        conn.close()
        # print('finally 这里执行了')

    return msg


def get_by_id(id, db_name):
    msg = ''
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # sql = "select name,url_m3u8 from movies where id=" + str(id)
        sql = "select name, content, magnet from movies where id=" + str(id)
        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        msg = '《' + rel[0][0] + '》 \n\n'
        msg += '\n- - - - - - - - - - - - - - - - - - \n'
        msg += rel[0][1]
        msg += '\n\n- - - - - - - - - - - - - - - - - - \n\n'
        chatper_list = rel[0][2].split('##')[:-1][:5]

        # 分割 磁力链接
        for url in chatper_list:
            if len(url):
                tag = url.split('#')
                msg += '<a href="' + tag[4] + '">【' + tag[2] + '】(' + tag[1] + ') ' + tag[0] + '</a>\n\n'
            else:
                pass
    except Exception as e:
        # print(e)
        msg = '你好，没有找到 ID 为 ' + str(id) + ' 的影片，请检查你的输入 ~'
    finally:
        # print('get_by_id finally 执行了')
        cursor.close()
        conn.close()

    return msg



def test():
    while 1:
        str_in = input('input:')
        str_rel = hello(str_in.strip())
        print(str_rel)
        print('----------------- next ------------')

# test()


# 让服务器监听在 0.0.0.0:80
# robot.config['HOST']='0.0.0.0'
# robot.config['PORT']=80
# robot.run()

