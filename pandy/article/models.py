from django.db import models
from django.utils import timezone

# Create your models here.
class Article(models.Model):
    title = models.CharField('标题', max_length = 255, blank = False)
    author = models.CharField('作者', max_length = 255, blank = False)
    article_type = models.CharField('类型', max_length = 255, blank = False)
    body = models.TextField('正文', blank = False)
    prior = models.IntegerField('显示优先级', default = 0)
    # 是否 可被 展示
    display = models.BooleanField('是否发布', default = False)
    article_views = models.PositiveIntegerField('阅读次数', default=0)
    article_pub_date = models.DateTimeField('新建时间', default=timezone.now())
    article_modefy_date = models.DateTimeField('上次修改时间', default=timezone.now())

    def __unicode__(self):
        return self.title

    # 阅读量自增加函数
    def increase_views(self):
        self.article_views += 1
        self.save(update_fields=['article_views'])
