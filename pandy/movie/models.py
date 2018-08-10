from django.db import models
from django.utils import timezone

# Create your models here.
class Movie(models.Model):
    v_href = models.CharField('采集页链接', max_length=255, blank=True)
    v_pic = models.CharField('封面图', max_length=255)
    v_name = models.CharField('电影名', max_length=255)
    v_text_info = models.TextField('影片介绍', default='影片信息暂时为空。', blank=True)
    v_bdpan = models.CharField('网盘链接', max_length=255)
    v_pass = models.CharField('密码', max_length=255, blank=True)

    v_ed2k_name = models.CharField('磁链1名称', max_length=255, default='磁力链接', blank=True)
    v_ed2k = models.CharField('磁力链接 1', max_length=255, blank=True)
    v_magnet_name =models.CharField('磁链2名称', max_length=255, default='磁力链接', blank=True)
    v_magnet = models.CharField('磁力链接 2', max_length=255, blank=True)
    v_valid = models.IntegerField('网盘链接是否可用', default=1)
    v_views = models.PositiveIntegerField('阅读次数', default=0)

    v_pub_date = models.DateTimeField('最后更新时间', default=timezone.now())

    def __unicode__(self):
        return self.v_name

    # 阅读量自增加函数
    def increase_views(self):
        self.v_views += 1
        self.save(update_fields=['v_views'])
