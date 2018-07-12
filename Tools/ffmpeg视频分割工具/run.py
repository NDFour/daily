# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-07-12 10:48:17
# Last Modified: 2018-07-12 11:55:53
#

import os
import time
import sys

class StartTime(object):

    def __init__(self):
        self.time='00:00:00'

    def add(self, addtime):
        # 获得上一次的时间
        time_list=self.time.split(':')
        # 将列表类型从 str 转为 int , 方便加减
        i_tmp=0
        for i in time_list:
            time_list[i_tmp]=int(i)
            i_tmp+=1

        time_list[2]+=int(addtime)
        
        # 时间加减
        while time_list[2]>59:
            time_list[2]=time_list[2] % 60
            time_list[1]+=1

        # 更新 self.time, 转换为 str
        self.time=''
        for i in time_list:
            print('>> time_list[%s]=%s' %(i, i))
            self.time+=str(i)+':'
        self.time=self.time[0:-1]
        print('>> 时间增加了 %s s, 现在是 %s' % (addtime, self.time) )


def exec_cmd(start_time, time_len, in_name, out_name):
    # start_time ; time_len ; in_name ; out_name
    raw_cmd = ('ffmpeg -ss %s -t %s -i %s  -c:a aac -strict experimental -b:a 98k videos/%s' % (start_time, time_len, in_name, out_name))
    print()
    print('>> %s' % raw_cmd)

    # input('按下回车开始分割')

    print()
    os.system(raw_cmd)

def main():
    print("        ffmpeg 视频分割工具")
    # 从命令行获取输入文件名
    in_name = sys.argv[1]
    time_len = input('每段视频长度：')
    for_times = input('需要的段数：')
    out_name = input('输出文件名：')
    name_tmp=out_name

    # 视频开始截取时间
    sTime=StartTime()
    print('>> 初始化时间： %s' %sTime.time)
    '''
    while(1):
        addtime=input('需要增加的秒数：')
        sTime.add(addtime)
        print('>> [main] ]增加之后的时间： %s' %sTime.time)
    '''

    for i in range(int(for_times)):
        out_name = out_name + str(i) + '.mp4'
        exec_cmd(sTime.time, time_len, in_name, out_name)
        print('第 %s 段视频分割完毕' % str(i))
        print()
        time.sleep(1)
        out_name = name_tmp
        sTime.add(time_len)
        print('下一段开始时间为: %s s' % sTime.time)

main()
