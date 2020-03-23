from django.contrib import admin
from .models import Overview, Information, Current

# Register your models here.
class OverviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

    # 后台点击修改信息页后展示的字段
    fieldsets = [
                ('基本信息', { 'fields' : ['name', 'menupage_total', 'movie_total', 'menupage_success', 'movie_success', 'menupage_fail', 'movie_fail', 'status'] } ),
                ]

class InformationAdmin(admin.ModelAdmin):
    list_display = ( 'stat', 'own', 'time')

    fieldsets = [
                ('消息', {'fields' : ['stat', 'own',  'info', 'url']}),
                ]

class CurrentAdmin(admin.ModelAdmin):
    list_display = ('current',)
    fieldsets = [
                ('当前爬虫', {'fields' : ['current']}),
                ]

admin.site.register(Overview, OverviewAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Current, CurrentAdmin)
