from django.contrib import admin
from .models import Onlineplay

# Register your models here.
class OnlineplayAdmin(admin.ModelAdmin):
    list_display = ('id', 'v_name', 'v_type', 'v_vip')

    fieldsets = [
            ('基本信息', {'fields': ['v_name', 'v_pic', 'v_playurl', 'v_text_info', 'v_href', 'v_belong_to', 'v_type', 'v_vip', 'v_views']}),
            ('时间戳', {'fields': ['v_pub_date']}),
    ]

    # 搜索
    search_fields = ('v_name', 'id')

admin.site.register(Onlineplay, OnlineplayAdmin)
