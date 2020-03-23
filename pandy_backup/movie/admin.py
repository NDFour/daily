from django.contrib import admin
from .models import Movie, Passwds

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'v_name', 'v_valid', 'v_pub_date')

    # 后台点击后修改信息页展示的字段
    fieldsets = [
            ('基本信息', { 'fields' : ['v_name', 'v_pic', 'v_text_info', 'v_bdpan', 'v_pass', 'v_valid', 'v_href', 'v_belong_to', 'v_views' ]}),
            ('磁力链接', { 'fields' : ['v_ed2k_name', 'v_ed2k', 'v_magnet_name', 'v_magnet']}),
            ('时间戳', {'fields' : ['v_pub_date']}),
            ]

    # 搜索功能
    search_fields = ('v_name','id',)

class PasswdsAdmin(admin.ModelAdmin):
    list_display = ('id', 'p_name', 'p_code', 'p_value')

# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Passwds, PasswdsAdmin)
