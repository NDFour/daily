# coding:utf-8
# djspider项目核心函数
# by werner 2017.04.13

# 引入django配置
# 为了使用 djange 提供的 model 的方法
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pandy.settings")
django.setup()

from time import sleep
from spidermonitor.models import *

### 全局变量，当前爬虫项目
global current_spider
current_spider = None

### 设置类
def setname(name):
    """设置爬虫的名字。若该名字的爬虫已存在，则直接取来用"""
    global current_spider
    try:
        current_spider = Overview.objects.get(name=name)
    except:
        #没找到说明不存在，新建一个
        current_spider = Overview.objects.create(name=name)
    #将当前爬虫写入Current表中，以此通知django当前爬虫是哪个
    try:
        c = Current.objects.get(id=1)
        c.current=current_spider
        c.save()
    except:
        Current.objects.create(id=1, current=current_spider)

def set_menupage_total(number):
    """修改当前爬虫目录页总量"""
    global current_spider
    current_spider.menupage_total=number
    current_spider.save()

def set_movie_total(number):
    global current_spider
    current_spider.movie_total=number
    current_spider.save()

### 状态类
def start():
    """开始"""
    global current_spider
    current_spider.status=1
    current_spider.save()

def paush(number):
    """暂停"""
    global current_spider
    current_spider.status=2
    current_spider.save()
    sleep(number)
    current_spider.status=1
    current_spider.save()

def finish():
    """完成"""
    global current_spider
    current_spider.status=3
    current_spider.save()

### 计数类
def add_menupage_succ():
    """目录页 成功任务数加一"""
    global current_spider
    current_spider.menupage_success = current_spider.menupage_success+1
    current_spider.save()

def add_movie_succ():
    global current_spider
    current_spider.movie_success = current_spider.movie_success+1
    current_spider.save()

def add_menupage_fail():
    """目录页 失败任务数加一"""
    global current_spider
    current_spider.menupage_fail = current_spider.menupage_fail+1
    current_spider.save()

def add_movie_fail():
    global current_spider
    current_spider.movie_fail = current_spider.movie_fail+1
    current_spider.save()

### 消息类
def printi(url, info, status):
    """传递一个消息"""
    global current_spider
    if status!=0 and status!=1:
        status=2
    Information.objects.create(url=url, info=info, stat=status, own=current_spider)
