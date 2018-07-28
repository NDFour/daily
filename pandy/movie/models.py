from django.db import models
from django.utils import timezone

# Create your models here.
class Movie(models.Model):
    v_href = models.CharField('采集页链接', max_length=255, blank=True)
    v_pic = models.CharField('封面图', max_length=255)
    v_name = models.CharField('电影名', max_length=255)
    v_bdpan = models.CharField('网盘链接', max_length=255)
    v_pass = models.CharField('密码', max_length=255, blank=True)
    v_ed2k = models.CharField('磁力链接 1', max_length=255, blank=True)
    v_magnet = models.CharField('磁力链接 2', max_length=255, blank=True)

    v_pub_date = models.DateTimeField('最后更新时间', default=timezone.now())

    def __unicode__(self):
        return self.v_name
