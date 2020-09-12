from celery import Celery
import time

# extract_voca.py
from . import extract_vocab
# stardict.py
# from . import stardict

celery_app = Celery('tasks', backend = 'redis://localhost', broker='redis://localhost')

# 测试用 
@celery_app.task
def add(x, y):
    time.sleep(6)
    return x + y


# 导出用户上传的 生词本 db 文件
'''
    file_path: 用户上传文件的存放路径 user_uploaded/11111.db
    mail_address: 用户接收邮箱地址
'''
@celery_app.task
def export_user_db(file_path, mail_address, user_message):
    '''
    print('进入 export_user_db task')
    print('file_path:')
    print(file_path)
    print('mail_address:')
    print(mail_address)
    '''

    input_file_path = './' + file_path
    output_file_path = './user_output/' + mail_address

    '''
    print('input_file_path:')
    print(input_file_path)
    print('output_file_path:')
    print(output_file_path)
    '''

    extract_vocab.main(input_file_path, output_file_path, mail_address, user_message)

    return '翻译 执行完毕！'


