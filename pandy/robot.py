from werobot import WeRoBot

robot=WeRoBot(token='wxweapilynn')
robot.config['SESSION_STORAGE'] = False

@robot.subscribe
def subscribe(message):
    return '看...又有一个有趣的灵魂关注了我们...👻\n\n----------\n\n谢谢关注！\n\n只要发送书籍📚的名字就可以了哦\n\n切记：可以名字不完整，但是一定不可以有错别字哦😯'


@robot.text
def hello(message):
    # 剑网专项行动
    # str_msg = '公众号搜索功能暂时下线了，正在调整中。敬请期待😊\n\n添加微信:\nndfour001，加入读书群。'
    # return str_msg
    
    if message.content.strip() == '获取暗号':
        return '0614'
    rel_info_text = '📚你好，这个是自动回复\n\n[玫瑰]书籍名字可以不完整\n[凋谢]但绝不可以有错别字哦，会搜不到的 ！\n\n'
    rel_info_a = '<a href="https://www.chenjin5.com/books/search/?book_name=' + message.content + '&book_search=book_search">点我查看[' + message.content + ']搜索结果</a>'
    return rel_info_text + rel_info_a


# 让服务器监听在　0.0.0.0:4444
# robot.config['HOST']='0.0.0.0'
# robot.config['PORT']=8000
# robot.run()
