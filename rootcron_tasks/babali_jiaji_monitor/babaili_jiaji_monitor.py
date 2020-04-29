import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import time

import requests
import os

def mail_babali_jiaji_csv():
    str_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 发邮件代码
    _user = "lgang219@qq.com"
    _pwd  = "eehrjkcueceqcaga"
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
    url = 'https://sc.ftqq.com/SCU52512T77e075b86690b62f884c8eeec4d6969f5cef37ed7855c.send'
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


def main():
    msg = ''
    msg += mail_babali_jiaji_csv()
    msg += '##########'
    msg += delete_babaili_cui_csv()

    if len(msg) > 10:
        pushtestmsg( msg )

main()
