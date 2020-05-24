from django.db import models
from django.utils import timezone

# Create your models here.
class Books(models.Model):
    book_title = models.CharField('书名', max_length=255, blank=False)
    book_pic = models.CharField('封面图', max_length=255)
    book_author = models.CharField('作者', max_length=255)
    book_category = models.CharField('图书类别', max_length=255, default='未分类')
    book_infos = models.TextField('图书信息（出版社等）')
    book_description = models.TextField('内容简介')
    book_origin = models.TextField('采集页')

    book_pan_1 = models.TextField('网盘链接 1', blank=True)
    book_pan_2 = models.TextField('网盘链接 2', blank=True)
    book_pan_3 = models.TextField('网盘链接 3', blank=True)
    book_pan_pass = models.CharField('网盘密码(1+2+3)', max_length=255, blank=True)
    book_rating = models.CharField('(豆瓣）评分', max_length=255)

    book_valid = models.IntegerField('网盘链接是否可用', default=1)
    book_views = models.PositiveIntegerField('阅读次数', default=0)

    book_pub_date = models.DateTimeField('更新时间', default=timezone.now())

    def __unicode__(self):
        return self.book_title

    # 阅读量自增加函数
    def increase_views(self):
        self.book_views += 1
        self.save(update_fields=['book_views'])


'''
# 网站通知
class Book_notify(models.Model):
    noty_title = models.CharField('标题', max_length = 255, blank = False)
    noty_author = models.CharField('发布人', max_length = 255, blank = False)
    noty_content = models.TextField('内容', blank = False)
    noty_date = models.DateTimeField('发布时间', default = timezone.now())

    def __unicode__(self):
        return self.noty_title
'''
