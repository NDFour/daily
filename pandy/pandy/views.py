from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from users.models import Users, Vip_code
import hashlib

# Create your views here.
def index(request):
    return render(request, 'index/index.html')

def login(request):
	# 根据 session 判断用户是否已经登录
	if request.session.get('is_login', None):
		return redirect('/')

	if request.method ==  'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		message = '请填写所有字段！'

		if username and password:
			username = username.strip()
			try:
				user = Users.objects.get(user_name = username)
				if user.user_passwd == hash_code(password):
					# 设置 session
					request.session['is_login'] = True
					request.session['user_id'] = user.id
					request.session['user_name'] = user.user_name
					request.session['user_isvip'] = user.user_isvip
					return redirect('/usercenter')
				else:
					message =  '密码不正确！'
			except:
				message = '用户名不存在！'

		return render(request, 'index/login.html', {'message': message})
	return render(request, 'index/login.html')

def logout(request):
	try:
		# 清空 session 信息
		request.session.flush()
	except:
		pass
	# request.session.flush()
	return redirect('/')

def user_center(request):
	username = request.session.get('user_name', default=None)
	if not username:
		return redirect('/login')
	try:
		user = Users.objects.get(user_name = username)
		# 充值后更新会员状态
		request.session['user_isvip'] = user.user_isvip
	except:
		user = None
		vip_type = ''
	return render(request, 'users/user_center.html', {'user': user})

def register(request):
	# 已登录状态下不可以注册
	if request.session.get('is_login', default=None):
		return redirect('/')

	if request.method == "POST":
		message = '请检查填写的内容！'
		username =  request.POST.get('username', None)
		password1 =  request.POST.get('password1', None)
		password2 =  request.POST.get('password2', None)
		try:
			contact = request.POST.get('contact', None)
		except:
			contact = '无'
		if password1 != password2:
			message = '两次输入的密码不一致！'
			return render(request, 'index/register.html', { 'message': message})
		else:
			same_name_user = Users.objects.filter(user_name = username)
			if same_name_user:
				message = '用户名已存在，请重新输入一个用户名！'
				return render(request, 'index/register.html', { 'message': message})
			# 通过检查，创建新用户
			new_user = Users()
			new_user.user_name = username
			new_user.user_passwd = hash_code(password1) # 加密密码保存
			new_user.user_contact = contact
			new_user.save()

			# return redirect('/login') # 跳转到登录页面
			return render(request, 'index/register.html', { 'message': '注册成功，现在去登录吧！', 'register_status': 'yes'})

	return render(request, 'index/register.html', locals()) # locals() 返回当前所有的本地变量字典

def activate_vip(request):
	if request.method ==  'POST':
		codestr = request.POST.get('vip_code', None)
		username = request.session.get('user_name', default=None)
		message = ''

		try:
			user = Users.objects.get(user_name = username)
		except:
			return render(request, '/')
		try:
			vip_code = Vip_code.objects.get( code_str = codestr )
		except:
			message = '激活码不存在！'
			return render(request, 'users/user_center.html', {"user": user, "message": message, 'vip_code': codestr})

		if vip_code.code_state:
			vip_code.code_state = 0
			try:
				user.user_vip_type += int(vip_code.code_type)
				user.user_isvip = 1
				message = '%s 天会员激活成功！' % str(vip_code.code_type)
			except:
				message = '更新会员天数出错，请联系管理员！'

			user.save()
			vip_code.save()
		else:
			message = '激活码已失效！'

		return render(request, 'users/user_center.html', {'user': user, 'message': message})
	return render(request, '/')


def hash_code(s, salt='tnt1024'):
	h = hashlib.sha256()
	s += salt
	h.update(s.encode()) # update 只接收 bytes 类型
	return h.hexdigest()