import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import csv
import time

import requests
import os

def mail_babali_jiaji_csv():
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 发邮件代码
    _user = "lgang219@qq.com"
    _pwd  = "xxxxxxxxxxxxxxxx"
    _to   = "ndfour@foxmail.com"

    try:
        msg = MIMEMultipart()
        msg["Subject"] = "[pandy 八百里加急] csv文件投递"
        msg["From"] = _user
        msg["To"] = _to

        msg.attach(MIMEText( '该邮件来自 [pandy 八百里加急催]\n\n' + str_time ) )

        # 添加附件
        attachment = MIMEApplication( open('/usr/bdpan_movie/daily/pandy/babaili_jiaji.csv', 'rb').read() )
        attachment.add_header('Content-Disposition', 'attachment', filename='babaili_jiaji_' + str_time + '.csv' )
        msg.attach( attachment )

        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()

        return ''
    except Exception as e:
        msg = '[邮件投递失败]'
        msg += str(e)

        return msg


# 删除 八百里加急催 生成的 csv 文件
def delete_babaili_cui_csv():
    try:
        cmd = 'rm /usr/bdpan_movie/daily/pandy/babaili_jiaji.csv'
        os.system( cmd )

        return ''
    except Exception as e:
        msg = '[delete_babaili_cui_csv 失败]'
        msg += str(e)
        return msg


# 推送消息到微信
def pushtestmsg(msg):
    url = 'https://sc.ftqq.com/SCUxxxxxxxxxxxxxxxxxxxxxxxxxxc.send'
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    desp = 'pandy 八百里加急 monitor 报警信息'
    data = {
        'text': desp,
        'desp': msg + '****' + str_time
        }
    try:
        r = requests.get( url, params = data )
        msg = 'Server酱 发送消息成功！！'
        print(msg)
    except Exception as e:
        msg = 'Server酱 发送消息失败，请重试！！'
        print(msg)


# 读取 babaili_jiaji.csv 中的信息 汇总到 本程序运行目录
def babaili_2_folder( babaili_path, folder_path):
    babaili_name = 'babaili_jiaji.csv'
    folder_name = 'out.csv'
    
    babaili_list = []
    try:
        with open( babaili_path + babaili_name, 'r', encoding = 'utf-8-sig' ) as f:
            reader = csv.reader(f)
            for line in reader:
                babaili_item = {}
                # print(type(line))
                # print(line)
                # print()
                if line:
                    babaili_item['book_name'] = line[0]
                    babaili_item['author'] = line[1]
                    babaili_item['contact_method'] = line[2]
                    babaili_item['other_info'] = line[3]
                    babaili_item['type'] = line[4]
                    babaili_item['time'] = line[5]
                    babaili_item['url'] = line[6]
                    babaili_list.append(babaili_item)
    except Exception as e:
        print('babaili_2_folder failed')
        print(e)
        return

    with open( folder_path + folder_name, 'a', encoding = 'utf-8-sig') as f:
        fieldnames = ['book_name', 'author', 'contact_method', 'other_info', 'type', 'time', 'url']
        writer = csv.DictWriter(f, fieldnames = fieldnames )
        for b_item in babaili_list:
            writer.writerow( b_item )



def main():
    babaili_path = '/usr/bdpan_movie/daily/pandy/'
    folder_path = '/root/rootcron_tasks/babali_jiaji_monitor/'
    babaili_2_folder( babaili_path, folder_path )

    msg = ''
    msg += mail_babali_jiaji_csv()
    msg += '##########'
    msg += delete_babaili_cui_csv()

    if len(msg) > 10:
        pushtestmsg( msg )

main()
