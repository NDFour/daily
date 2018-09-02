# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Overview(models.Model):
    name = models.CharField('Spider name', max_length=255, default='spidername', unique=True)
    menupage_total = models.PositiveIntegerField('Menupage num', default=0)
    movie_total = models.PositiveIntegerField('Movie num', default=0)  #[0 ,2147483647]
    menupage_success = models.PositiveIntegerField('Menu page crawled', default=0)  #[0 ,2147483647]
    movie_success = models.PositiveIntegerField('Movie crawled', default=0)  #[0 ,2147483647]
    menupage_fail = models.PositiveIntegerField('Menupage failed', default=0)  #[0 ,2147483647]
    movie_fail = models.PositiveIntegerField('Movie failed', default=0)  #[0 ,2147483647]
    status = models.PositiveIntegerField('Status', default=0)  #0:未开始；1:运行中；2:暂停中；3:已完成；其他:未知状态

    def __unicode__(self):
        return self.name
    '''
    class Meta:
        # 给模型起一个可读的名字，一般定义为中文
        verbose_name = '总览表'
        # 可读名字的复数形式
        verbose_name_plural = '总览表'
    '''

class Information(models.Model):
    url = models.CharField('URL', max_length=500, blank=True, null=True)
    info = models.TextField('Msg', blank=True, null=True)
    stat = models.PositiveIntegerField('Msg type', default=0)  #0，成功；1：警告；2：错误；
    own = models.ForeignKey(Overview, verbose_name='Belong to', blank=True, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField('Time', auto_now=True)    #每次保存时该自动会自动更新为当前时间

    def __unicode__(self):
        return self.url
    '''
    class Meta:
        verbose_name = '消息表'
        verbose_name_plural = '消息表'
    '''

class Current(models.Model):
    current = models.ForeignKey(Overview, verbose_name='Current spider', blank=True, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return 'Current spider'
    '''
    class Meta:
        verbose_name = '当前爬虫'
        verbose_name_plural = u'当前爬虫'
    '''
