from werobot import WeRoBot
import pymysql
import traceback

import re
import time

import requests

robot=WeRoBot(token='wxweapilynn')
# robot.config['SESSION_STORAGE'] = False


@robot.subscribe
def subscribe(message, session):
    # return ('看...又有一个有趣的灵魂关注了我们...👻\n\n----------\n\n⚠️ 注意：\n[%s]如果您取关公众号，以后即便再次关注也无法获取暗号哦\n\n如有需要，联系管理员：ndfour001' %(session.get('unsubscribe_cnt', 0) ) )
    return ('看...又有一个有趣的灵魂关注了我们...👻\n')


@robot.unsubscribe
def unsubscribe(message, session):
    tmp_cnt = session.get('unsubscribe_cnt', 0) + 1
    session['unsubscribe_cnt'] = tmp_cnt
    # return ('取关次数 %s' %(tmp_cnt) )


@robot.text
def hello(message, session):
    # 常量
    is_system_pause = 1

    if message.content == 'gettime':
        return 'reset ' + str( int(time.time()) + 5432112345)
    # 重置用户取关次数
    elif re.compile(r"^reset \d{10,}$").match(message.content.strip()):
        user_time = int( message.content.split(' ')[1] )
        now_time = int(time.time())
        # 10 分钟内有效
        cmp_rel = now_time - (user_time - 5432112345)
        if (cmp_rel > 0) and (cmp_rel < 600):
            session['unsubscribe_cnt'] = 0
            return '重置用户取关次数成功！'
        else:
            try:
                # debug_msg = ( "%s = %s - %s - %s" %(str(cmp_rel), str(user_time), '5432112345', str(now_time) ) )
                return ('超时，请在获取激活码后 10分钟之内完成激活操作。\n')
            except Exception as e:
                return str(e)
    
    # 网页图书详情页 暗号
    an_hao = ''
    if session.get('unsubscribe_cnt', 0) > 0:
        an_hao = ('⚠️ [%s] 取关后即便再次关注也将无法获取暗号，如有需要请联系管理员：ndfour001' %(session.get('unsubscribe_cnt', 0) ) )
    else:
        an_hao = '本期暗号：7130\n\n把暗号输入到网页上的输入框提交即可 😁'

    # 管理员微信
    admin_wechat = 'ndfour001'

    # 剑网专项行动
    # str_msg = '公众号搜索功能暂时下线了，正在调整中。敬请期待😊\n\n添加微信:\n' + admin_wechat + '，加入读书群。'
    # return str_msg
    
    if is_system_pause:
        if session.get('unsubscribe_cnt', 0) > 0:
            return ('⚠️ [%s] 取关次数过多，无法下载，如有需要请联系管理员：ndfour001' %(session.get('unsubscribe_cnt', 0) ) )

        return reply_single(message, session).replace('lanzous', 'lanzoux')
    else:
        if message.content.strip() == '获取暗号':
            return an_hao
        else:
            rel_info_text = '📚你好，这个是自动回复\n\n[玫瑰]书籍名字可以不完整\n[凋谢]但绝不可以有错别字哦，会搜不到的 ！\n\n'
            rel_info_a = '<a href="https://www.chenjin5.com/books/search/?book_name=' + message.content + '&book_search=book_search">点我查看[' + message.content + ']搜索结果</a>'
            rel_an_hao = '\n\n==================\n\n' + an_hao
            return rel_info_text + rel_info_a + rel_an_hao


'''
2020.11.2
关闭网站，仅保留公众号搜书，并返回下载链接
'''
def reply_single(message, session):
    str_input = message.content.strip()
    msg = ''
    try:
        # 该回复为 图书 ID
        str_input = int(str_input)

        rel_note = ''
        # rel_note = '\n\n= = = = = = = = = = = = = = = =\n\n'
        # rel_note += '⚠️ 如果你搜索的书名为<a>纯数字</a>，如 1984，请务必记得加书名号《1984》'

        # 根据 ID 搜索 详情
        statusCode, msg = get_by_id(str_input)
        msg += rel_note

        # if finded book
        if statusCode:
            # 检查用户发送消息是否过于频繁
            if isToMany(message, session):
                return '你今天已经下载了好多书啦 ~\n\n要记得看呀，明天再来下载吧\n\nps: 取关无法重置当天下载次数，反而会导致以后都无法下载'

    except Exception as e:
        traceback.print_exc()
        '''
        # 该回复为 书名
        # 若 将用户发送消息 转为 int 失败，则表示 用户发送的是 书名，而不是 图书 ID
        '''
        # msg = '1. 查看电子书下载链接请输入网页上提供的【下载码】，下载码为纯数字\n\n2. 搜索电子书请点 <a href="https://www.chenjin5.com"> 搜索</a>'

        msg = '<a href="https://www.chenjin5.com/books/search/?book_name=' + message.content + '&book_search=book_search">点我查看[' + message.content + ']搜索结果</a>'

    # msg = format_rel_msg(msg)

    return msg

'''
对返回的消息规格化，删除或替换某些字符
'''
def format_rel_msg(msg):
    msg = msg.replace('/epub+mobi+azw3', '')
    msg = msg.replace('epub+mobi+azw3', '')
    msg = msg.replace('mobi+epub+azw3', '')
    msg = msg.replace('mobi+epub', '')
    msg = msg.replace('epub+mobi', '')

    msg = msg.replace('《', '')
    msg = msg.replace('》', '')

    return msg


def get_rel(name):
    # 回复给用户的消息体
    msg = ''
    try:
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='xqksj', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        sql = "SELECT id, book_title, book_author FROM books_books WHERE book_title" + " LIKE '%" + name + "%' ORDER BY LENGTH(book_title) LIMIT 25"

        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

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
            msg = '发送书名前编码获得下载链接（无需带括号）。\n\n'
            msg += '搜索 《' + name + '》 的结果: '+ str( len(rel) ) + '条\n- - - - - - - - - - - - - - - - - - \n\n'
            for m in rel:
                author = str(m[2]).strip().replace('请参考图书详情','').replace('暂无','')
                if author:
                    msg += '[ ' + str(m[0]) + ' ] ' + str(m[1]).strip() + '-' + author + '\n\n'
                else:
                    msg += '[ ' + str(m[0]) + ' ] ' + str(m[1]).strip() + '\n\n'
            msg += '\n- - - - - - - - - - - - - - - - - - \n\n'
            msg += '⚠️ 名字可以不完整，但是一定不要有错别字哦 ~'

        else:
            msg = '你好，没有找到跟《' + name + '》相符合的图书哦\n你可以换一本书试试~~~'
    except Exception as e:
        # print(e)
        msg = '你好，没有找到跟《' + name + '》相符合的图书哦\n你可以换一本书试试~~~'
    finally:
        cursor.close()
        conn.close()
        # print('finally 这里执行了')

    return msg


def get_by_id(id):
    # 0: not found
    # 1: finded
    statusCode = 0

    msg = ''
    try:
        conn = pymysql.connect('127.0.0.1', port=3306, user='root', password='xqksj', db='bdpan', charset='utf8')
        cursor = conn.cursor()

        # sql = "select name,url_m3u8 from movies where id=" + str(id)
        sql = "SELECT id, book_title, book_pan_1, book_pan_2, book_pan_3, book_pan_pass FROM books_books WHERE id = " + str(id)

        # print(sql)
        cursor.execute(sql)
        rel = cursor.fetchall()

        msg = 'ID: ' + str(rel[0][0]) + '\n\n'
        msg += '书名： ' + str(rel[0][1]) + '\n\n'
        msg += '下载链接：\n'
        msg += '- - - - - - - - - - - - - - - - - - \n'

        for url in rel[0][2:5]:
            if url:
                url_sp = url.split('##')
                msg += str(url_sp[0]) + ' 下载:\n'
                msg += str(url_sp[-1]) + '\n\n'
            else:
                pass
        # 提取码
        if (len(rel[0][5])):
            msg += str(rel[0][5]) + '\n\n'

        msg += '\n= = = = = = = = = = = = = = = =\n\n'
        # msg += '⚠️ 微信内不支持下载电子书文件，否则会<a>乱码</a>，请复制下载链接到浏览器内下载。'
        msg += '⚠️  强烈建议把下载链接复制到浏览器打开\n⚠️微信内直接点开极有可能访问不了。'

        statusCode = 1

    except Exception as e:
        # print(e)
        # traceback.print_exc()
        msg = '\n\n你好，没有找到 ID 为 ' + str(id) + ' 的图书，请检查你的输入 ~\n\n'
        # msg += '⚠️ 如果果片名为纯数字，在发送书名的时候请加上书名号，如《1984》，其中 1984 为书名，否则会搜索不出结果'
    finally:
        # print('get_by_id finally 执行了')
        cursor.close()
        conn.close()

    return statusCode, msg


    

'''
判断用户是否在 1天 内发送过多消息
'''
def isToMany(message, session):
    # 用户发送消息总数 +1
    totalSendMsg = session.get('total_msg_count', 0)
    session['total_msg_count'] = (totalSendMsg + 1)

    # 用户上次发送消息的时间
    lastTime = session.get('last_time', '')
    todayTime = time.strftime("%Y-%m-%d", time.localtime())

    # 用户已发消息数 +1
    sendedMsg = session.get('sended_msg', 0)
    if todayTime == lastTime:
        sendedMsg += 1
    else:
        # 当天消息数清零
        sendedMsg = 0
        session['last_time'] = todayTime

    session['sended_msg'] = sendedMsg

    cntLimit = 10
    if sendedMsg > cntLimit:
        # wechatMsg('古德毛宁李 有人发送超过 ' + str(cntLimit) + ' 条消息', 'source:%s\n\ncontent:%s' % (message.source, message.content) )
        return True

    return False



def wechatMsg(title, msg):
    wechat_url = ''
    notify_data = {
        'text': title,
        'desp': msg,
    }
    try:
        r = requests.get( wechat_url, params = notify_data, timeout = 30 )
    except Exception as e:
        traceback.print_exc()



def main():
    while 1:
        msg = input('msg:')
        rel = hello(msg)
        print(rel)
        print('################')

# main()


# 让服务器监听在　0.0.0.0:4444
# robot.config['HOST']='0.0.0.0'
# robot.config['PORT']=80
# robot.run()
