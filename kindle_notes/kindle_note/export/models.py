from django.db import models
from django.utils import timezone

# Create your models here.
class Upload_Record(models.Model):
	file_name = models.CharField('上传文件名', max_length = 255, blank = False)
	mail_addr = models.CharField('邮箱', max_length = 50, blank = False)
	message = models.TextField('备注/留言', blank = True)
	export_info = models.TextField('转换信息', default = '空')
	mail_state = models.CharField('邮件状态', max_length = 255, blank = False, default = '空')
	upload_time = models.DateTimeField('上传时间', default = timezone.now())

	def __unicode__(self):
		return self.mail_addr


