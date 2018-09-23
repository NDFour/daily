from django.db import models
from django.utils import timezone

# Create your models here.
class Onlineplay(models.Model):
    v_href = models.CharField('采集页链接', max_length=255, blank=True)
    v_pic = models.CharField('封面图', max_length=255)
    v_name = models.CharField('电影名', max_length=255)
    v_text_info = models.TextField('影片介绍', default='影片介绍暂时为空', blank=True)
    v_playurl = models.TextField('播放链接', blank=True)
    v_views = models.PositiveIntegerField('浏览次数', default=0)
    v_pub_date = models.DateTimeField('更新时间', default=timezone.now())
    v_belong_to = models.PositiveIntegerField('影片类别（网盘/在线）', default=2, blank=True)
    v_type = models.PositiveIntegerField('类型', default=1) # 战争，剧情，科幻
    v_vip = models.IntegerField('vip视频', default=0) # 0: not vip; 1: only for vip

    def __unicode__(self):
        return self.v_name
    # 阅读量自增函数
    def increase_views(self):
        self.v_views += 1
        self.save(update_fields=['v_views'])
