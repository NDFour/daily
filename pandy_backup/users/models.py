from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
	user_name = models.CharField('用户名', max_length=125, unique=True) # 用户名必须唯一
	user_passwd = models.CharField('密码', max_length=256)
	user_contact = models.CharField('联系方式', max_length=256, default='无', blank=True)
	user_isvip = models.IntegerField('是否vip', default=0)
	user_creat_time = models.DateTimeField(auto_now_add=True) # 用户注册时间
	user_vip_type = models.IntegerField('会员类型', default=0) # 1天会员，3天会员，7天会员等，根据充值卡类型区分

	def __unicode__(self):
		return self.user_name

class Vip_code(models.Model):
	code_str = models.CharField('激活码', max_length=256)
	code_type = models.IntegerField('类型（天数)', default=0)
	code_state = models.IntegerField('是否可用', default=0)

	def __unicode__(self):
		return self.code_str

