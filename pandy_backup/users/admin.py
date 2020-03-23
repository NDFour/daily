from django.contrib import admin
from .models import  Users, Vip_code

# Register your models here.
class UsersAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_name', 'user_isvip', 'user_vip_type' )

class Vip_codeAdmin(admin.ModelAdmin):
	list_display = ('id', 'code_str', 'code_type', 'code_state')

admin.site.register(Users, UsersAdmin)
admin.site.register(Vip_code, Vip_codeAdmin)
